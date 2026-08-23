from datetime import datetime
from uuid import UUID

import pytest

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.pulse_candidate import PulseCandidate
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)


def event(identity: int, timestamp: float, source: int = 1):
    candidate_id = UUID(int=identity + 100)
    return ElementaryMetricEvent(
        id=UUID(int=identity),
        contributor_id=UUID(int=source + 10),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime(2026, 1, 1),
        sound_source_id=UUID(int=source),
        supporting_pulse_candidate_ids=(candidate_id,),
        temporal_scope="[0,20)",
        evidence_status="OBSERVATION_SUPPORTED",
        materialization_rule="source-observation-event/v1",
        source_asset_sha256=f"asset-{source}",
    )


def candidate(item):
    return PulseCandidate(
        id=item.supporting_pulse_candidate_ids[0],
        sound_source_id=item.sound_source_id,
        timestamp=item.timestamp,
        strength=1.0,
        confidence=1.0,
        created_at=datetime(2026, 1, 1),
        observation_index=item.id.int,
        observation_provenance_id=f"observation-{item.id.int}",
    )


def build(targets, drums):
    all_events = (*targets, *drums)
    return DrumRelativeEMELocalizationBuilder().build(
        targets,
        drums,
        tuple(candidate(item) for item in all_events),
        temporal_origin_seconds=0.0,
        analysis_execution_id="test-execution",
    )


def test_normal_boundaries_distances_fraction_and_provenance():
    target, first, second = event(1, 12.0, 2), event(2, 10.0), event(3, 14.0)
    result = build((target,), (first, second))[0]
    assert result.preceding_drum_eme.eme_id == first.id
    assert result.following_drum_eme.eme_id == second.id
    assert result.distance_from_preceding_seconds == 2.0
    assert result.distance_from_following_seconds == -2.0
    assert result.nearest_drum_eme.eme_id == first.id
    assert result.nearest_selection_status == "EQUAL_DISTANCE_TIE"
    assert result.observed_interval_fraction == 0.5
    assert result.target_supporting_observations[0].observation_index == 1
    assert result.nearest_drum_eme.supporting_observations[0].observation_index == 2
    assert result.localization_rule == "observed-drum-eme-relative-localization/v1"


def test_before_first_and_after_last_have_null_interval_fraction():
    first, last = event(10, 10.0), event(11, 20.0)
    before, after = event(1, 5.0, 2), event(2, 25.0, 2)
    earlier, later = build((before, after), (first, last))
    assert earlier.preceding_drum_eme is None
    assert earlier.following_drum_eme.eme_id == first.id
    assert earlier.nearest_displacement_seconds == -5.0
    assert earlier.observed_interval_fraction is None
    assert later.preceding_drum_eme.eme_id == last.id
    assert later.following_drum_eme is None
    assert later.nearest_displacement_seconds == 5.0
    assert later.observed_interval_fraction is None


def test_exact_timestamp_equality_uses_equal_drum_as_preceding_and_nearest():
    target, equal, following = event(1, 10.0, 2), event(2, 10.0), event(3, 20.0)
    result = build((target,), (equal, following))[0]
    assert result.preceding_drum_eme.eme_id == equal.id
    assert result.following_drum_eme.eme_id == following.id
    assert result.nearest_drum_eme.eme_id == equal.id
    assert result.nearest_displacement_seconds == 0.0
    assert result.observed_interval_fraction == 0.0


def test_duplicate_drum_timestamps_are_preserved_and_deterministic():
    target = event(9, 10.0, 2)
    duplicate_high, duplicate_low = event(5, 10.0), event(4, 10.0)
    results = build((target,), (duplicate_high, duplicate_low))
    replay = build((target,), (duplicate_low, duplicate_high))
    assert results == replay
    assert results[0].preceding_drum_eme.eme_id == duplicate_high.id
    assert results[0].nearest_drum_eme.eme_id == duplicate_low.id
    assert results[0].nearest_selection_status == "EQUAL_DISTANCE_TIE"
    assert results[0].observed_interval_fraction is None


def test_order_is_deterministic_and_missing_lineage_is_rejected():
    first, second = event(1, 2.0, 2), event(2, 1.0, 2)
    drum = event(3, 0.0)
    results = build((first, second), (drum,))
    assert tuple(item.target_eme_id for item in results) == (second.id, first.id)
    with pytest.raises(ValueError, match="Missing PulseCandidate lineage"):
        DrumRelativeEMELocalizationBuilder().build(
            (first,), (drum,), (), temporal_origin_seconds=0.0,
            analysis_execution_id="test-execution",
        )


@pytest.mark.parametrize(
    "timestamp,expected",
    [(30.4274, "00:00:30.427"), (30.4275, "00:00:30.428"), (3661.001, "01:01:01.001")],
)
def test_absolute_time_formatting(timestamp, expected):
    assert DrumRelativeEMELocalizationBuilder.format_absolute_time(timestamp) == expected
