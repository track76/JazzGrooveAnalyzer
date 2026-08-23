from collections import Counter
from uuid import NAMESPACE_URL, uuid5

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)
from jga.representation.builders.rhythm_section_timing_profile_builder import (
    RhythmSectionTimingProfileBuilder,
)
from jga.representation.rhythm_section_timing_profile import AnalyticalRoleAssignment


SOURCES = (
    ("Drums", "drums.wav", 63, "TEMPORAL_REFERENCE"),
    ("Piano", "piano.wav", 49, "ACCOMPANIMENT"),
    ("Double Bass", "double_bass.wav", 27, "ACCOMPANIMENT"),
    ("Tenor Sax", "tenor_sax.wav", 16, "OUTSIDE_CURRENT_CORE"),
)


def test_controlled_rhythm_section_profile_preserves_authorized_population():
    analyses = {
        name: AnalysisPipeline().analyze(f"recordings/validation/stems/{filename}")
        for name, filename, _, _ in SOURCES
    }
    events = tuple(
        event for analysis in analyses.values()
        for event in analysis.elementary_metric_events
    )
    drums = analyses["Drums"].elementary_metric_events
    targets = tuple(
        event for name in ("Piano", "Double Bass", "Tenor Sax")
        for event in analyses[name].elementary_metric_events
    )
    candidates = tuple(
        candidate for analysis in analyses.values()
        for candidate in analysis.domain_pulse_candidates
    )
    localizations = DrumRelativeEMELocalizationBuilder().build(
        targets, drums, candidates, temporal_origin_seconds=0.0,
        analysis_execution_id="controlled-profile-localization",
    )
    assignments = []
    for name, _, _, role in SOURCES:
        sample = analyses[name].elementary_metric_events[0]
        assignments.append(
            AnalyticalRoleAssignment(
                assignment_id=uuid5(NAMESPACE_URL, f"controlled-role:{name}"),
                source_id=sample.sound_source_id,
                asset_id=sample.source_asset_sha256,
                temporal_scope=sample.temporal_scope,
                temporal_origin_seconds=0.0,
                role=role,
                assignment_rule="pi-authorized-controlled-role/v1",
                execution_id="controlled-role-execution",
                scientific_authority_id="AD-040",
                scientific_authority_fingerprint="b8983e8",
            )
        )
    assignments.append(
        AnalyticalRoleAssignment(
            assignment_id=uuid5(NAMESPACE_URL, "controlled-role:Voice"),
            source_id=uuid5(NAMESPACE_URL, "controlled-source:Voice"),
            asset_id="voice-deferred", temporal_scope=events[0].temporal_scope,
            temporal_origin_seconds=0.0, role="DEFERRED",
            assignment_rule="pi-authorized-controlled-role/v1",
            execution_id="controlled-role-execution", scientific_authority_id="AD-040",
            scientific_authority_fingerprint="b8983e8",
        )
    )
    builder = RhythmSectionTimingProfileBuilder()
    first = builder.build(
        events, localizations, assignments,
        temporal_scope=events[0].temporal_scope, temporal_origin_seconds=0.0,
        execution_id="controlled-profile", provenance_id="CED-VAL-001",
        scientific_authority_ids=("AD-037", "AD-038", "AD-040"),
    )
    second = builder.build(
        reversed(events), reversed(localizations), reversed(assignments),
        temporal_scope=events[0].temporal_scope, temporal_origin_seconds=0.0,
        execution_id="controlled-profile", provenance_id="CED-VAL-001",
        scientific_authority_ids=("AD-040", "AD-038", "AD-037"),
    )
    name_by_event = {
        event.id: name for name, analysis in analyses.items()
        for event in analysis.elementary_metric_events
    }
    assert first == second
    assert len(first.temporal_reference_events) == 63
    assert Counter(
        name_by_event[item.target_eme.id]
        for item in first.accompaniment_relationships
    ) == {"Piano": 49, "Double Bass": 27}
    assert len(first.accompaniment_relationships) == 76
    assert all(item.correspondence.status == "GEOMETRIC_ONLY" for item in first.accompaniment_relationships)
    assert len(events) == 155
    assert len(localizations) == 92
    assert len(analyses["Tenor Sax"].elementary_metric_events) == 16
    assert all(analysis.declared_metric_reference is None for analysis in analyses.values())
    assert all(analysis.declared_meter is None for analysis in analyses.values())
