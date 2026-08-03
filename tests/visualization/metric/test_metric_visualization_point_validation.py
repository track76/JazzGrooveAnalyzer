from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)


def test_metric_visualization_point_is_valid():

    point = MetricVisualizationPoint(
        time=1.0,
        value=0.5,
    )

    assert point.is_valid()
