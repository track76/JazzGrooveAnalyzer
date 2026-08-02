from tests.support.domain_objects import make_metric_cluster

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)
from jga.representation.metric_point import MetricPoint
from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)
from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
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
            axis=METRIC_TEMPORAL_DISPLACEMENT_AXIS,
            value=0.0,
        ),
    )

    portrait = MetricClusterPortrait(
        metric_cluster=cluster,
        points=(point,),
    )

    assert portrait.points == (point,)
