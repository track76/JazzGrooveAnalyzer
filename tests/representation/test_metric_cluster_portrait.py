from tests.support.domain_objects import make_metric_cluster

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.metric_point import MetricPoint
from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


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
        coordinate=ScientificCoordinate(
            value=0.0,
            unit="milliseconds",
            dimension="metric_temporal_displacement",
        ),
    )

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(point,),
    )

    assert portrait.points == (point,)
