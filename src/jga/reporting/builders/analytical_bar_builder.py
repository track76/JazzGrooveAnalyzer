from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)

from jga.reporting.analytical_bar import (
    AnalyticalBar,
)


class AnalyticalBarBuilder:
    """
    Builds one AnalyticalBar from reconstructed
    metric information.

    The builder performs only representational
    translation and does not reconstruct data.
    """

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
    ) -> AnalyticalBar:
        """
        Translates one ReconstructedMeasure into
        one AnalyticalBar preserving scientific data.
        """

        return self.build(

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

        )
