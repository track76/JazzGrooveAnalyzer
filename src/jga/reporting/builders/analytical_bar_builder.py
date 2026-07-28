from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)

from jga.domain.metric_contributor import (
    MetricContributor,
)

from jga.domain.sound_source import (
    SoundSource,
)

from jga.reporting.analytical_bar import (
    AnalyticalBar,
)

from jga.reporting.builders.analytical_beat_builder import (
    AnalyticalBeatBuilder,
)


class AnalyticalBarBuilder:
    """
    Builds one AnalyticalBar from reconstructed
    metric information.

    The builder performs only representational
    translation and does not reconstruct data.
    """

    def __init__(self):

        self.beat_builder = (
            AnalyticalBeatBuilder()
        )

    def build(
        self,
        number: int,
        start_time_seconds: float,
        end_time_seconds: float,
        time_signature: str,
        internal_bpm: float,
    ) -> AnalyticalBar:

        return AnalyticalBar(

            number=number,

            start_time_seconds=start_time_seconds,

            end_time_seconds=end_time_seconds,

            time_signature=time_signature,

            internal_bpm=internal_bpm,

            beats=(),

        )

    def build_from_measure(
        self,
        measure: ReconstructedMeasure,
        metric_contributors: tuple[MetricContributor, ...] = (),
        sound_sources: tuple[SoundSource, ...] = (),
    ) -> AnalyticalBar:
        """
        Translates one ReconstructedMeasure into
        one AnalyticalBar preserving scientific data.
        """

        beats = []

        for reference in measure.beat_references:

            clusters = tuple(
                cluster
                for cluster in measure.metric_clusters
                if cluster.beat_reference.id
                == reference.id
            )

            if clusters:

                beats.append(

                    self.beat_builder.build(

                        reference=reference,

                        number=reference.index + 1,

                        metric_cluster=clusters[0],

                        metric_contributors=(
                            metric_contributors
                        ),

                        sound_sources=(
                            sound_sources
                        ),

                    )

                )

            else:

                beats.append(

                    self.beat_builder.build(

                        reference=reference,

                        number=reference.index + 1,

                    )

                )


        return AnalyticalBar(

            number=measure.number,

            start_time_seconds=(
                measure.start_time_seconds
            ),

            end_time_seconds=(
                measure.end_time_seconds
            ),

            time_signature=(
                measure.time_signature
            ),

            internal_bpm=(
                measure.internal_bpm
            ),

            beats=tuple(beats),

        )
