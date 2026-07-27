from jga.domain.metric_cluster import (
    MetricCluster,
)

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.services.metric_offset_calculator import (
    MetricOffsetCalculator,
)

from jga.reporting.analytical_cell import (
    AnalyticalCell,
)


class AnalyticalCellBuilder:
    """
    Builds AnalyticalCell representations from
    scientific metric observations.
    """

    def __init__(self):

        self.offset_calculator = (
            MetricOffsetCalculator()
        )

    def build(
        self,
        cluster: MetricCluster,
        event: ElementaryMetricEvent,
    ) -> AnalyticalCell:

        offset_ms = (
            self.offset_calculator.compute(
                event,
                cluster.beat_reference,
            )
        )

        return AnalyticalCell(

            instrument="Unknown",

            beat=(
                cluster.beat_reference.index
            ),

            metric_cluster_id=(
                cluster.id
            ),

            absolute_time_seconds=(
                event.timestamp
            ),

            internal_bpm=0.0,

            offset_ms=offset_ms,

            delta_ms=0.0,

            significant_change=False,

        )
