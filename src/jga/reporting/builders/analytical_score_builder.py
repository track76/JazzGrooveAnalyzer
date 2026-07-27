from jga.runtime.analysis_context import AnalysisContext

from jga.reporting.analytical_score import (
    AnalyticalScore,
)

from jga.reporting.builders.analytical_bar_builder import (
    AnalyticalBarBuilder,
)


class AnalyticalScoreBuilder:
    """
    Builds the Analytical Score from the
    AnalysisContext produced by the JGA pipeline.

    Reporting layer only translates existing
    scientific results.
    """

    def __init__(self):

        self.bar_builder = (
            AnalyticalBarBuilder()
        )

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalyticalScore:

        title = "Unknown"

        if context.audio is not None:
            title = context.audio.path.name

        bars = tuple(

            self.bar_builder.build_from_measure(
                measure
            )

            for measure
            in context.reconstructed_measures

        )

        return AnalyticalScore(

            title=title,

            artist="Unknown",

            bars=bars,

        )
