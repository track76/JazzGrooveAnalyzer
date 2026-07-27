from jga.reporting.analytical_score import (
    AnalyticalScore,
)


class AnalyticalScoreCompiler:
    """
    Compiles the scientific analysis into an
    AnalyticalScore.

    Renderers never compute scientific data.
    """

    def compile(
        self,
        title: str,
        artist: str,
    ) -> AnalyticalScore:

        return AnalyticalScore(

            title=title,

            artist=artist,

            bars=(),

        )

