from collections import Counter

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)


SOURCES = (
    ("Drums", "drums.wav", 63),
    ("Piano", "piano.wav", 49),
    ("Double Bass", "double_bass.wav", 27),
    ("Tenor Sax", "tenor_sax.wav", 16),
)


def test_complete_population_projects_without_metric_context():
    analyses = {
        name: AnalysisPipeline().analyze(
            f"recordings/validation/stems/{filename}"
        )
        for name, filename, _ in SOURCES
    }
    drums = analyses["Drums"].elementary_metric_events
    targets = tuple(
        event
        for name in ("Piano", "Double Bass", "Tenor Sax")
        for event in analyses[name].elementary_metric_events
    )
    candidates = tuple(
        candidate
        for analysis in analyses.values()
        for candidate in analysis.domain_pulse_candidates
    )
    builder = DrumRelativeEMELocalizationBuilder()
    first = builder.build(
        targets, drums, candidates,
        temporal_origin_seconds=0.0,
        analysis_execution_id="controlled-test",
    )
    second = builder.build(
        reversed(targets), reversed(drums), reversed(candidates),
        temporal_origin_seconds=0.0,
        analysis_execution_id="controlled-test",
    )
    source_name = {
        event.id: name
        for name, analysis in analyses.items()
        for event in analysis.elementary_metric_events
    }

    assert sum(len(item.elementary_metric_events) for item in analyses.values()) == 155
    assert len(drums) == 63
    assert len(first) == len(targets) == 92
    assert len({item.target_eme_id for item in first}) == 92
    assert {item.target_eme_id for item in first} == {item.id for item in targets}
    assert Counter(source_name[item.target_eme_id] for item in first) == {
        "Piano": 49, "Double Bass": 27, "Tenor Sax": 16,
    }
    assert first == second
    assert all(item.target_supporting_observations for item in first)
    assert all(item.nearest_drum_eme.supporting_observations for item in first)
    assert all(analysis.declared_metric_reference is None for analysis in analyses.values())
    assert all(analysis.declared_meter is None for analysis in analyses.values())
    # Legacy analyses may independently produce BeatReference output. The new
    # projection accepts only EME and PulseCandidate evidence and is unchanged
    # by that unrelated output.
    assert all(item.localization_rule == builder.RULE for item in first)
