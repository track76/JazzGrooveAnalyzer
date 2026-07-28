from jga.domain.beat_reference import (
    BeatReference,
)

from jga.domain.metric_cluster import (
    MetricCluster,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.sound_source import (
    SoundSource,
)

from jga.reporting.analytical_beat import (
    AnalyticalBeat,
)

from jga.reporting.builders.analytical_cell_builder import (
    AnalyticalCellBuilder,
)


class AnalyticalBeatBuilder:
    """
    Builds one AnalyticalBeat from one
    reconstructed BeatReference.

    The builder performs only representational
    translation.
    """

    def __init__(self):

        self.cell_builder = (
            AnalyticalCellBuilder()
        )

    def build_from_reference(
        self,
        reference: BeatReference,
    ) -> AnalyticalBeat:
        """
        Preserves the source BeatReference identity.
        """

        return AnalyticalBeat(

            number=reference.index,

            timestamp_seconds=(
                reference.timestamp
            ),

            cells=(),

        )

    def build(
        self,
        reference: BeatReference,
        number: int,
        metric_cluster: MetricCluster | None = None,
        metric_contributors: tuple[MetricContributor, ...] = (),
        sound_sources: tuple[SoundSource, ...] = (),
    ) -> AnalyticalBeat:
        """
        Builds an AnalyticalBeat using a local
        beat number inside an AnalyticalBar.

        If a MetricCluster is provided, its
        ElementaryMetricEvents are translated
        into AnalyticalCells.
        """

        cells = ()

        if metric_cluster is not None:

            cells = tuple(

                self.cell_builder.build(
                    metric_cluster,
                    event,
                    metric_contributors=metric_contributors,
                    sound_sources=sound_sources,
                )

                for event in (
                    metric_cluster.events
                )

            )

        return AnalyticalBeat(

            number=number,

            timestamp_seconds=(
                reference.timestamp
            ),

            cells=cells,

        )
