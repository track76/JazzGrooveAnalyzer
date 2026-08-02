from tests.support.domain_objects import (
    make_metric_cluster,
)

from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)

from jga.representation.metric_point import MetricPoint

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


def test_metric_points_belong_to_metric_cluster():

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
        coordinate=ScientificCoordinate(
            value=0.0,
            unit="milliseconds",
            dimension="metric_temporal_displacement",
        ),
    )

    assert point.event is cluster.events[0]
