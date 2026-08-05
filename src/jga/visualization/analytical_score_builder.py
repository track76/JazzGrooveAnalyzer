"""
Analytical Score Builder.

Builds immutable AnalyticalScore objects.
"""

from jga.visualization.analytical_score import (
    AnalyticalScore,
)


class AnalyticalScoreBuilder:
    """
    Builds musicological analytical scores.

    M72.
    """

    def build(
        self,
    ) -> AnalyticalScore:

        return AnalyticalScore(
            recording_title="",
            artist="",
            time_signature="4/4",
            average_bpm=120.0,
            sections=(),
            measures=(),
            instrument_lanes=(),
        )
