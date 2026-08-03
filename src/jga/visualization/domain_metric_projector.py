"""
Domain Metric Projector.

Projects the metric domain into a
MetricVisualizationSeries.
"""

from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)
from jga.visualization.metric_visualization_point import (
    MetricVisualizationPoint,
)
from jga.visualization.metric_visualization_series import (
    MetricVisualizationSeries,
)


class DomainMetricProjector:
    """
    Projects an InternalMetricTimeline into a
    MetricVisualizationSeries.
    """

    def project(
        self,
        timeline: InternalMetricTimeline,
    ) -> MetricVisualizationSeries:
        """
        Creates a visualization series from the
        metric domain.
        """

        points: list[MetricVisualizationPoint] = []

        for pulse in timeline.pulses:
            for event in pulse.cluster.events:
                points.append(
                    MetricVisualizationPoint(
                        time=event.timestamp,
                        value=event.confidence,
                    )
                )

        return MetricVisualizationSeries(
            points=tuple(points),
        )
