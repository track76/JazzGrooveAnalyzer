from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster
from jga.domain.services.metric_cluster_builder import (
    MetricClusterBuilder,
)


def make_event(timestamp: float) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
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


def test_default_cluster_window():
    builder = MetricClusterBuilder()

    assert builder.cluster_window == 0.010


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

    builder = MetricClusterBuilder(cluster_window=0.010)

    beat = make_beat(1.000)

    e1 = make_event(0.998)
    e2 = make_event(1.004)

    clusters = builder.build((beat,), (e1, e2))

    assert len(clusters) == 1
    assert clusters[0].events == (e1, e2)

def test_build_clusters_with_multiple_beat_references():

    builder = MetricClusterBuilder(cluster_window=0.010)

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

def test_events_outside_cluster_window_are_ignored():

    builder = MetricClusterBuilder(cluster_window=0.010)

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
    assert clusters[0].events == (e1, e2)

def test_beat_reference_without_events_does_not_create_cluster():

    builder = MetricClusterBuilder(cluster_window=0.010)

    beat_references = (
        make_beat(1.000, index=1),
        make_beat(1.500, index=2),
    )

    e1 = make_event(1.001)

    clusters = builder.build(
        beat_references,
        (e1,),
    )

    assert len(clusters) == 1

    assert clusters[0].beat_reference == beat_references[0]
    assert clusters[0].events == (e1,)


def test_no_clusters_created_when_no_events_match_any_beat():

    builder = MetricClusterBuilder(cluster_window=0.010)

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

    assert clusters == ()