from jga.runtime.analysis_context import AnalysisContext

from jga.reporting.analytical_score import (
    AnalyticalScore,
)


class AnalyticalScoreBuilder:
    """
    Builds the Analytical Score from the
    AnalysisContext produced by the JGA pipeline.
    """

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalyticalScore:

        title = "Unknown"

        if context.audio is not None:
            title = context.audio.path.name

        return AnalyticalScore(

            title=title,

            artist="Unknown",

            bars=(),

        )

