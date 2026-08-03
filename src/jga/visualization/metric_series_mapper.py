"""
Metric Series Mapper.

Maps metric visualization series
into graphic representation.
"""

from jga.visualization.graphic_element import (
    GraphicElement,
)

from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)


class MetricSeriesMapper:
    """
    Maps metric series to graphic elements.
    """

    def map(
        self,
        series: MetricVisualizationSeries,
    ) -> GraphicElement:
        """
        Creates graphic representation.
        """

        return GraphicElement(
            element_type="metric_series",
            metadata={
                "points": len(series.points),
            },
        )
