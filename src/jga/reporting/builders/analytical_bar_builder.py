from jga.reporting.analytical_bar import (
    AnalyticalBar,
)


class AnalyticalBarBuilder:
    """
    Builds one AnalyticalBar from one reconstructed
    Metric Cluster.
    """

    def build(
        self,
        number: int,
        time_seconds: float,
        time_signature: str,
        internal_bpm: float,
    ) -> AnalyticalBar:

        return AnalyticalBar(

            number=number,

            time_seconds=time_seconds,

            time_signature=time_signature,

            internal_bpm=internal_bpm,

            beats=(),

        )

