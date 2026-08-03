from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)

from jga.visualization.metric_series_mapper import (
    MetricSeriesMapper,
)


def test_metric_series_mapper_exists():

    mapper = MetricSeriesMapper()

    element = mapper.map(
        MetricVisualizationSeries(),
    )

    assert element is not None
