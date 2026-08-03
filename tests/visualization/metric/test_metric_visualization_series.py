from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)

from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)


def test_metric_visualization_series_exists():

    point = MetricVisualizationPoint(
        time=1.0,
        value=0.5,
    )

    series = MetricVisualizationSeries(
        points=(
            point,
        ),
    )

    assert series.points[0] is point
