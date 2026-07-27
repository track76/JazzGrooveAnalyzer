from jga.domain.beat_reference import (
    BeatReference,
)

from jga.reporting.analytical_beat import (
    AnalyticalBeat,
)


class AnalyticalBeatBuilder:
    """
    Builds one AnalyticalBeat from one
    reconstructed BeatReference.

    The builder performs only representational
    translation.
    """

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
    ) -> AnalyticalBeat:
        """
        Builds an AnalyticalBeat using a local
        beat number inside an AnalyticalBar.
        """

        return AnalyticalBeat(

            number=number,

            timestamp_seconds=(
                reference.timestamp
            ),

            cells=(),

        )
