from jga.domain.metric_cluster import (
    MetricCluster,
)

from jga.domain.elementary_metric_event import (
    ElementaryMetricEvent,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.sound_source import (
    SoundSource,
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

    Reporting translation only.
    """

    def __init__(self):

        self.offset_calculator = (
            MetricOffsetCalculator()
        )

    def _resolve_instrument(
        self,
        contributor_id,
        metric_contributors,
        sound_sources,
    ) -> str:

        contributor = next(
            (
                item
                for item in metric_contributors
                if item.id == contributor_id
            ),
            None,
        )

        if contributor is None:
            return "Unknown"

        source = next(
            (
                item
                for item in sound_sources
                if item.id == contributor.sound_source_id
            ),
            None,
        )

        if source is None:
            return "Unknown"

        return source.name

    def build(
        self,
        cluster: MetricCluster,
        event: ElementaryMetricEvent,
        metric_contributors: tuple[MetricContributor, ...] = (),
        sound_sources: tuple[SoundSource, ...] = (),
    ) -> AnalyticalCell:

        offset_ms = (
            self.offset_calculator.compute(
                event,
                cluster.beat_reference,
            )
        )

        return AnalyticalCell(

            instrument=(
                self._resolve_instrument(
                    event.contributor_id,
                    metric_contributors,
                    sound_sources,
                )
            ),

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
