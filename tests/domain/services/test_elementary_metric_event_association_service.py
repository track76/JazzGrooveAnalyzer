from datetime import datetime
from uuid import uuid4

from jga.domain.beat_reference import BeatReference
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate
from jga.domain.services.elementary_metric_event_association_service import (
    ElementaryMetricEventAssociationService,
)


def fixtures(timestamps=(1.0,)):
    source_id = uuid4()
    contributor = MetricContributor(
        id=uuid4(),
        sound_source_id=source_id,
        musical_function_id=uuid4(),
        active=True,
        created_at=datetime.now(),
    )
    candidates = tuple(
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_id,
            timestamp=timestamp,
            strength=1.0,
            confidence=0.8,
            created_at=datetime.now(),
        )
        for timestamp in timestamps
    )
    beat = BeatReference(
        id=uuid4(),
        index=0,
        timestamp=1.0,
        created_at=datetime.now(),
        supporting_pulse_candidate_ids=tuple(item.id for item in candidates),
        reconstruction_rule="test-movement/v1",
        temporal_scope="complete_recording",
    )
    return contributor, candidates, beat


def test_one_observation_associates_once_with_full_identity_lineage():
    contributor, candidates, beat = fixtures()
    results = ElementaryMetricEventAssociationService().associate(
        candidates, (contributor,), (beat,)
    )

    assert len(results) == 1
    assert results[0].outcome == "ASSOCIATED"
    assert results[0].supporting_pulse_candidate_ids == (candidates[0].id,)
    assert results[0].beat_reference_id == beat.id
    assert results[0].contributor_id == contributor.id


def test_distinct_positions_for_one_contributor_and_movement_are_ambiguous():
    contributor, candidates, beat = fixtures((1.0, 1.01))
    results = ElementaryMetricEventAssociationService().associate(
        candidates, (contributor,), (beat,)
    )

    assert len(results) == 1
    assert results[0].outcome == "AMBIGUOUS"
    assert results[0].timestamp is None


def test_unassociated_observations_are_not_consumed_or_synthesized():
    contributor, candidates, beat = fixtures()
    unrelated_beat = BeatReference(
        id=uuid4(), index=1, timestamp=2.0, created_at=datetime.now()
    )

    results = ElementaryMetricEventAssociationService().associate(
        candidates, (contributor,), (unrelated_beat,)
    )

    assert results == ()
    assert len(candidates) == 1


def test_one_observation_is_not_duplicated_across_movements():
    contributor, candidates, first_beat = fixtures()
    second_beat = BeatReference(
        id=uuid4(),
        index=1,
        timestamp=2.0,
        created_at=datetime.now(),
        supporting_pulse_candidate_ids=(candidates[0].id,),
    )

    results = ElementaryMetricEventAssociationService().associate(
        candidates, (contributor,), (first_beat, second_beat)
    )

    assert len(results) == 2
    assert all(item.outcome == "AMBIGUOUS" for item in results)
