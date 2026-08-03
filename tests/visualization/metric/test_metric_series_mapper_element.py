from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)

from jga.visualization.metric_series_mapper import (
    MetricSeriesMapper,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_mapper_returns_graphic_element():

    element = MetricSeriesMapper().map(
        MetricVisualizationSeries(),
    )

    assert isinstance(
        element,
        GraphicElement,
    )
