from dataclasses import FrozenInstanceError
from datetime import datetime
from uuid import UUID

import pytest

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.pulse_candidate import PulseCandidate
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)
from jga.representation.builders.rhythm_section_timing_profile_builder import (
    RhythmSectionTimingProfileBuilder,
)
from jga.representation.rhythm_section_timing_profile import (
    AnalyticalRoleAssignment,
    AuthorizedEventRelationReference,
    CalibrationEvidenceReference,
    EventCorrespondence,
)


SCOPE = "[0,20)"


def event(identity: int, timestamp: float, source: int, asset: str):
    return ElementaryMetricEvent(
        id=UUID(int=identity), contributor_id=UUID(int=source + 100),
        timestamp=timestamp, confidence=1.0, created_at=datetime(2026, 1, 1),
        sound_source_id=UUID(int=source),
        supporting_pulse_candidate_ids=(UUID(int=identity + 1000),),
        temporal_scope=SCOPE, evidence_status="OBSERVATION_SUPPORTED",
        materialization_rule="source-observation-event/v1",
        source_asset_sha256=asset,
    )


def candidate(item):
    return PulseCandidate(
        id=item.supporting_pulse_candidate_ids[0], sound_source_id=item.sound_source_id,
        timestamp=item.timestamp, strength=1.0, confidence=1.0,
        created_at=datetime(2026, 1, 1), observation_index=item.id.int,
        observation_provenance_id=f"observation-{item.id.int}",
    )


def assignment(identity, source, asset, role):
    return AnalyticalRoleAssignment(
        assignment_id=UUID(int=identity), source_id=UUID(int=source), asset_id=asset,
        temporal_scope=SCOPE, temporal_origin_seconds=0.0, role=role,
        assignment_rule="pi-authorized-role/v1", execution_id="role-execution",
        scientific_authority_id="AD-040", scientific_authority_fingerprint="ad040-fp",
    )


@pytest.fixture
def authority():
    drum = event(1, 1.0, 1, "drum-asset")
    piano = event(2, 1.1, 2, "piano-asset")
    bass = event(3, 0.9, 3, "bass-asset")
    sax = event(4, 1.2, 4, "sax-asset")
    events = (drum, piano, bass, sax)
    localizations = DrumRelativeEMELocalizationBuilder().build(
        (piano, bass, sax), (drum,), tuple(candidate(item) for item in events),
        temporal_origin_seconds=0.0, analysis_execution_id="localization-execution",
    )
    roles = (
        assignment(11, 1, "drum-asset", "TEMPORAL_REFERENCE"),
        assignment(12, 2, "piano-asset", "ACCOMPANIMENT"),
        assignment(13, 3, "bass-asset", "ACCOMPANIMENT"),
        assignment(14, 4, "sax-asset", "OUTSIDE_CURRENT_CORE"),
        assignment(15, 5, "voice-asset", "DEFERRED"),
    )
    return events, localizations, roles


def build(authority, **overrides):
    events, localizations, roles = authority
    arguments = dict(
        events=events, drum_relative_localizations=localizations,
        role_assignments=roles, temporal_scope=SCOPE, temporal_origin_seconds=0.0,
        execution_id="profile-execution", provenance_id="profile-provenance",
        scientific_authority_ids=("AD-037", "AD-038", "AD-040"),
    )
    arguments.update(overrides)
    return RhythmSectionTimingProfileBuilder().build(**arguments)


def test_profile_is_immutable_and_reuses_raw_objects(authority):
    profile = build(authority)
    with pytest.raises(FrozenInstanceError):
        profile.temporal_scope = "changed"
    events, localizations, _ = authority
    assert profile.temporal_reference_events[0] is events[0]
    assert profile.accompaniment_relationships[0].drum_relative_localization in localizations
    assert all(not hasattr(item, "corrected_timestamp") for item in profile.accompaniment_relationships)
    assert all(not hasattr(item, "corrected_displacement") for item in profile.accompaniment_relationships)


def test_identity_replay_and_order_are_deterministic(authority):
    first = build(authority)
    events, localizations, roles = authority
    second = build((tuple(reversed(events)), tuple(reversed(localizations)), tuple(reversed(roles))))
    assert first == second
    assert first.profile_id == second.profile_id
    assert first.scientific_fingerprint == second.scientific_fingerprint
    assert tuple(item.target_eme.timestamp for item in first.accompaniment_relationships) == (0.9, 1.1)


def test_roles_are_explicit_and_instrument_name_cannot_assign(authority):
    profile = build(authority)
    assert {item.role for item in profile.role_assignments} == {
        "TEMPORAL_REFERENCE", "ACCOMPANIMENT", "OUTSIDE_CURRENT_CORE", "DEFERRED"
    }
    events, localizations, _ = authority
    with pytest.raises(ValueError, match="exactly one temporal-reference"):
        RhythmSectionTimingProfileBuilder().build(
            events, localizations, (), temporal_scope=SCOPE,
            temporal_origin_seconds=0.0, execution_id="x", provenance_id="x",
            scientific_authority_ids=("AD-040",),
        )


def test_current_core_includes_reference_and_accompaniment_only(authority):
    profile = build(authority)
    assert tuple(item.id.int for item in profile.temporal_reference_events) == (1,)
    assert {item.target_eme.id.int for item in profile.accompaniment_relationships} == {2, 3}
    assert all(item.target_eme.id.int != 4 for item in profile.accompaniment_relationships)
    assert any(item.role == "DEFERRED" for item in profile.role_assignments)


def test_geometric_localization_does_not_authorize_correspondence(authority):
    profile = build(authority)
    assert all(
        item.correspondence.status == "GEOMETRIC_ONLY"
        and item.correspondence.authorized_relation is None
        for item in profile.accompaniment_relationships
    )
    with pytest.raises(ValueError, match="independent evidence"):
        EventCorrespondence("AUTHORIZED_EVENT_RELATION")
    assert {EventCorrespondence(status).status for status in (
        "GEOMETRIC_ONLY", "UNRESOLVED", "NOT_APPLICABLE"
    )} == {"GEOMETRIC_ONLY", "UNRESOLVED", "NOT_APPLICABLE"}


def test_authorized_relation_requires_matching_provenance_bound_events(authority):
    events, _, _ = authority
    evidence = AuthorizedEventRelationReference(
        evidence_id="relation-1", target_eme_id=events[1].id,
        drum_eme_id=events[0].id, authority_id="GT-CONTROL",
        scientific_fingerprint="relation-fingerprint",
    )
    profile = build(
        authority,
        correspondence_by_target={
            events[1].id: EventCorrespondence("AUTHORIZED_EVENT_RELATION", evidence)
        },
    )
    piano = next(item for item in profile.accompaniment_relationships if item.target_eme.id == events[1].id)
    assert piano.correspondence.authorized_relation is evidence


def test_calibration_context_is_separate_and_cannot_change_raw(authority):
    events, localizations, roles = authority
    calibration = CalibrationEvidenceReference(
        evidence_id="pairwise-calibration", experiment_id="H-PAIRWISE",
        scientific_fingerprint="calibration-fingerprint", source_pair_type="Piano–Drums",
        classification="NO_DETECTABLE_PAIRWISE_BIAS", applicability_status="APPLICABLE",
        applicability_conditions=("controlled asset binding",),
        uncertainty_evidence_id="bootstrap-intervals",
        source_role_assignment_id=roles[1].assignment_id,
        reference_role_assignment_id=roles[0].assignment_id,
    )
    target_timestamp = events[1].timestamp
    displacement = next(item for item in localizations if item.target_eme_id == events[1].id).nearest_displacement_seconds
    profile = build(authority, calibration_by_assignment={roles[1].assignment_id: calibration})
    relationship = next(item for item in profile.accompaniment_relationships if item.target_eme.id == events[1].id)
    assert relationship.calibration_evidence is calibration
    assert relationship.correspondence.status == "GEOMETRIC_ONLY"
    assert relationship.target_eme.timestamp == target_timestamp
    assert relationship.drum_relative_localization.nearest_displacement_seconds == displacement


def test_provenance_and_absolute_time_require_no_metric_inputs(authority):
    profile = build(authority)
    assert profile.temporal_origin_seconds == 0.0
    assert profile.temporal_scope == SCOPE
    assert profile.projection_rule == "rhythm-section-timing-profile/v1"
    assert profile.execution_id == "profile-execution"
    assert profile.provenance_id == "profile-provenance"
    assert profile.scientific_authority_ids == ("AD-037", "AD-038", "AD-040")
    assert not hasattr(profile, "bpm")
    assert not hasattr(profile, "meter")
    assert not hasattr(profile, "measures")
