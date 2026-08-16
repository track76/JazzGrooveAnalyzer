from datetime import datetime
from uuid import uuid4

from jga.domain.elementary_metric_event_association import (
    ElementaryMetricEventAssociation,
)
from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)
from jga.domain.metric_contributor import MetricContributor
from jga.domain.pulse_candidate import PulseCandidate


def association(outcome="ASSOCIATED", timestamp=1.25):
    return ElementaryMetricEventAssociation(
        beat_reference_id=uuid4(),
        contributor_id=uuid4(),
        sound_source_id=uuid4(),
        supporting_pulse_candidate_ids=(uuid4(),),
        timestamp=timestamp if outcome == "ASSOCIATED" else None,
        confidence=0.9 if outcome == "ASSOCIATED" else None,
        temporal_scope="complete_recording",
        association_rule="test-rule/v1",
        outcome=outcome,
    )


def test_builder_materializes_authorized_association_with_lineage():
    item = association()
    events = ElementaryMetricEventBuilder().build((item,))

    assert len(events) == 1
    event = events[0]
    assert event.beat_reference_id == item.beat_reference_id
    assert event.contributor_id == item.contributor_id
    assert event.sound_source_id == item.sound_source_id
    assert event.supporting_pulse_candidate_ids == item.supporting_pulse_candidate_ids
    assert event.association_rule == item.association_rule
    assert event.timestamp == item.timestamp


def test_builder_does_not_materialize_ambiguous_or_absent_association():
    events = ElementaryMetricEventBuilder().build(
        (association("AMBIGUOUS"), association("NOT_PRODUCED"))
    )

    assert events == ()


def test_builder_identity_is_deterministic():
    item = association()
    first = ElementaryMetricEventBuilder().build((item,))[0]
    second = ElementaryMetricEventBuilder().build((item,))[0]

    assert first.id == second.id


def test_source_event_materialization_precedes_and_ignores_metric_association():
    source_id = uuid4()
    contributor = MetricContributor(
        uuid4(), source_id, uuid4(), True, datetime.now()
    )
    candidates = tuple(
        PulseCandidate(
            id=uuid4(),
            sound_source_id=source_id,
            timestamp=timestamp,
            strength=1.0,
            confidence=0.9,
            created_at=datetime.now(),
            observation_index=index,
            observation_provenance_id="asset",
        )
        for index, timestamp in enumerate((1.0, 1.1, 1.2))
    )
    builder = ElementaryMetricEventBuilder()

    first = builder.build_from_observations(
        candidates, (contributor,), "[0,2)", "a" * 64
    )
    second = builder.build_from_observations(
        candidates, (contributor,), "[0,2)", "a" * 64
    )

    assert len(first) == len(candidates)
    assert tuple(item.id for item in first) == tuple(item.id for item in second)
    assert all(item.beat_reference_id is None for item in first)
    assert all(len(item.supporting_pulse_candidate_ids) == 1 for item in first)
