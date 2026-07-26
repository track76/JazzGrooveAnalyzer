from tests.support.domain_objects import (
    make_elementary_metric_event,
    make_metric_cluster,
)

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.metric_point import MetricPoint


def test_metric_points_belong_to_metric_cluster():

    cluster = make_metric_cluster()

    point = MetricPoint(
        event=cluster.events[0],
        offset_ms=0.0,
    )

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(point,),
    )

    assert point.event in portrait.metric_cluster.events


def test_empty_portrait_is_allowed():

    cluster = make_metric_cluster()

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(),
    )

    assert portrait.points == ()


def test_metric_point_keeps_original_event_reference():

    cluster = make_metric_cluster()

    point = MetricPoint(
        event=cluster.events[0],
        offset_ms=0.0,
    )

    assert point.event is cluster.events[0]
