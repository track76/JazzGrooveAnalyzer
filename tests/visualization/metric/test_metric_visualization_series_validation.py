from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)

from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)


def test_metric_visualization_series_is_valid():

    series = MetricVisualizationSeries(
        points=(
            MetricVisualizationPoint(
                time=1.0,
                value=0.5,
            ),
        ),
    )

    assert series.is_valid()
