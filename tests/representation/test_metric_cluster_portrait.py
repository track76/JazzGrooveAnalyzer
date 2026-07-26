from tests.support.domain_objects import make_metric_cluster

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.metric_point import MetricPoint


def test_metric_cluster_portrait_type_exists():
    assert MetricClusterPortrait is not None


def test_metric_cluster_portrait_preserves_cluster_reference():

    cluster = make_metric_cluster()

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(),
    )

    assert portrait.metric_cluster is cluster
    assert portrait.points == ()


def test_metric_cluster_portrait_accepts_metric_points():

    cluster = make_metric_cluster()

    point = MetricPoint(
        event=cluster.events[0],
        offset_ms=0.0,
    )

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(point,),
    )

    assert portrait.points == (point,)
