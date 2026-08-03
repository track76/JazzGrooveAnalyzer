from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)

from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)

from jga.visualization.metric_series_mapper import (
    MetricSeriesMapper,
)


def test_mapper_preserves_metric_information():

    series = MetricVisualizationSeries(
        points=(
            MetricVisualizationPoint(
                time=1.0,
                value=0.5,
            ),
        ),
    )

    element = MetricSeriesMapper().map(
        series,
    )

    assert element.metadata["points"] == 1
