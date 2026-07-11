from datetime import datetime
from uuid import uuid4

import pytest

from jga.domain.beat_reference import BeatReference
from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.services.pulse_builder import PulseBuilder


def make_beat(timestamp: float, index: int = 0) -> BeatReference:
    return BeatReference(
        id=uuid4(),
        index=index,
        timestamp=timestamp,
        created_at=datetime.now(),
    )


def make_event(timestamp: float) -> ElementaryMetricEvent:
    return ElementaryMetricEvent(
        id=uuid4(),
        contributor_id=uuid4(),
        timestamp=timestamp,
        confidence=1.0,
        created_at=datetime.now(),
    )


def make_cluster(
    timestamp: float,
    index: int = 0,
) -> MetricCluster:
    return MetricCluster(
        id=uuid4(),
        beat_reference=make_beat(timestamp, index),
        events=(
            make_event(timestamp),
        ),
        created_at=datetime.now(),
    )


def test_builder_can_be_instantiated():

    assert PulseBuilder() is not None

def test_build_requires_argument():

    builder = PulseBuilder()

    with pytest.raises(TypeError):
        builder.build()    

def test_empty_input_returns_empty_tuple():

    builder = PulseBuilder()

    assert builder.build(()) == ()

def test_single_cluster_creates_single_pulse():

    builder = PulseBuilder()

    cluster = make_cluster(
        timestamp=1.000,
        index=0,
    )

    pulses = builder.build((cluster,))

    assert len(pulses) == 1

    assert isinstance(pulses[0], Pulse)

    assert pulses[0].cluster == cluster

    assert pulses[0].index == 0

    assert pulses[0].timestamp == 1.000

def test_build_multiple_clusters_creates_multiple_pulses():

    builder = PulseBuilder()

    cluster1 = make_cluster(
        timestamp=0.500,
        index=1,
    )

    cluster2 = make_cluster(
        timestamp=1.000,
        index=2,
    )

    cluster3 = make_cluster(
        timestamp=1.500,
        index=3,
    )

    pulses = builder.build((cluster1, cluster2, cluster3))

    assert len(pulses) == 3

    assert pulses[0].index == 1
    assert pulses[1].index == 2
    assert pulses[2].index == 3

    assert pulses[0].timestamp == 0.500
    assert pulses[1].timestamp == 1.000
    assert pulses[2].timestamp == 1.500

    assert pulses[0].cluster is cluster1
    assert pulses[1].cluster is cluster2
    assert pulses[2].cluster is cluster3

def test_build_preserves_input_order():

    builder = PulseBuilder()

    cluster3 = make_cluster(
        timestamp=3.000,
        index=3,
    )

    cluster1 = make_cluster(
        timestamp=1.000,
        index=1,
    )

    cluster2 = make_cluster(
        timestamp=2.000,
        index=2,
    )

    pulses = builder.build(
        (
            cluster3,
            cluster1,
            cluster2,
        )
    )

    assert [pulse.index for pulse in pulses] == [3, 1, 2]

    assert pulses[0].cluster is cluster3
    assert pulses[1].cluster is cluster1
    assert pulses[2].cluster is cluster2

def test_build_large_number_of_clusters():

    builder = PulseBuilder()

    clusters = tuple(
        make_cluster(
            timestamp=float(i),
            index=i,
        )
        for i in range(100)
    )

    pulses = builder.build(clusters)

    assert len(pulses) == 100

    assert pulses[0].index == 0
    assert pulses[-1].index == 99

    assert pulses[0].cluster is clusters[0]
    assert pulses[-1].cluster is clusters[-1]