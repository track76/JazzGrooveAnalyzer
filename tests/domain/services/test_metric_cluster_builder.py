from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster
from jga.domain.services.metric_cluster_builder import (
    MetricClusterBuilder,
)


def make_event(
    timestamp: float,
    beat_reference_id=None,
) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
        beat_reference_id=beat_reference_id,
    )


def make_beat(timestamp: float, index: int = 0) -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
    )


def test_builder_can_be_instantiated():
    assert MetricClusterBuilder() is not None


def test_builder_uses_existing_projection_engine():
    builder = MetricClusterBuilder()

    from jga.domain.services.beat_projection_engine import BeatProjectionEngine

    assert isinstance(builder._projection_engine, BeatProjectionEngine)


def test_build_requires_arguments():
    builder = MetricClusterBuilder()

    with pytest.raises(TypeError):
        builder.build()


def test_empty_input_returns_empty_tuple():
    builder = MetricClusterBuilder()

    assert builder.build((), ()) == ()


def test_single_event_creates_single_cluster():

    builder = MetricClusterBuilder()

    beat = make_beat(1.000)

    event = make_event(1.000)

    clusters = builder.build((beat,), (event,))

    assert len(clusters) == 1
    assert isinstance(clusters[0], MetricCluster)
    assert clusters[0].events == (event,)


def test_events_assigned_to_same_beat_create_one_cluster():

    builder = MetricClusterBuilder()

    beat = make_beat(1.000)

    e1 = make_event(0.998)
    e2 = make_event(1.004)

    clusters = builder.build((beat,), (e1, e2))

    assert len(clusters) == 1
    assert clusters[0].events == (e1, e2)


def test_build_clusters_with_multiple_beat_references():

    builder = MetricClusterBuilder()

    beat_references = (
        make_beat(1.000, index=1),
        make_beat(1.500, index=2),
    )

    e1 = make_event(0.998)
    e2 = make_event(1.003)
    e3 = make_event(1.499)

    clusters = builder.build(
        beat_references,
        (e1, e2, e3),
    )

    assert len(clusters) == 2

    assert clusters[0].beat_reference == beat_references[0]
    assert clusters[0].events == (e1, e2)

    assert clusters[1].beat_reference == beat_references[1]
    assert clusters[1].events == (e3,)


def test_distant_events_are_projected_and_never_discarded():

    builder = MetricClusterBuilder()

    beat_references = (
        make_beat(1.000, index=1),
    )

    e1 = make_event(0.998)
    e2 = make_event(1.003)
    e3 = make_event(1.050)

    clusters = builder.build(
        beat_references,
        (e1, e2, e3),
    )

    assert len(clusters) == 1
    assert clusters[0].events == (e1, e2, e3)


def test_beat_reference_without_events_creates_empty_cluster():

    builder = MetricClusterBuilder()

    beat_references = (
        make_beat(1.000, index=1),
        make_beat(1.500, index=2),
    )

    e1 = make_event(1.001)

    clusters = builder.build(
        beat_references,
        (e1,),
    )

    assert len(clusters) == 2

    assert clusters[0].beat_reference == beat_references[0]
    assert clusters[0].events == (e1,)

    assert clusters[1].beat_reference == beat_references[1]
    assert clusters[1].events == ()


def test_every_event_projects_to_the_nearest_available_beat():

    builder = MetricClusterBuilder()

    beat_references = (
        make_beat(1.000, index=1),
        make_beat(2.000, index=2),
    )

    events = (
        make_event(3.000),
    )

    clusters = builder.build(
        beat_references,
        events,
    )

    assert len(clusters) == 2
    assert clusters[0].events == ()
    assert clusters[1].events == events


def test_exact_tie_projects_deterministically_to_earlier_beat():
    builder = MetricClusterBuilder()
    earlier = make_beat(1.0, index=1)
    later = make_beat(2.0, index=2)
    event = make_event(1.5)

    first = builder.build((later, earlier), (event,))
    second = builder.build((later, earlier), (event,))

    assert first[0].beat_reference is earlier
    assert first[0].events == (event,)
    assert first[1].events == ()
    assert tuple(cluster.events for cluster in first) == tuple(
        cluster.events for cluster in second
    )


def test_every_event_appears_once_with_identity_and_timestamp_preserved():
    builder = MetricClusterBuilder()
    beats = (make_beat(1.0, 1), make_beat(2.0, 2), make_beat(3.0, 3))
    events = (make_event(0.2), make_event(1.7), make_event(4.8))

    clusters = builder.build(beats, events)
    projected = tuple(event for cluster in clusters for event in cluster.events)

    assert len(projected) == len(events)
    assert {event.id for event in projected} == {event.id for event in events}
    assert {event.id: event.timestamp for event in projected} == {
        event.id: event.timestamp for event in events
    }


def test_authorized_movement_identity_precedes_nearest_reprojection():
    earlier = make_beat(1.0, 1)
    later = make_beat(2.0, 2)
    event = make_event(1.1, beat_reference_id=later.id)

    clusters = MetricClusterBuilder().build((earlier, later), (event,))

    assert clusters[0].events == ()
    assert clusters[1].events == (event,)


def test_unknown_authorized_movement_is_rejected():
    beat = make_beat(1.0, 1)
    event = make_event(1.0, beat_reference_id=uuid4())

    with pytest.raises(ValueError, match="outside the supplied timeline"):
        MetricClusterBuilder().build((beat,), (event,))
