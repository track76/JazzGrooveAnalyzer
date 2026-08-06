"""
=========================================================
Jazz Groove Analyzer (JGA)

Analytical Score Runner

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext

from jga.visualization.analytical_score_builder import (
    AnalyticalScoreBuilder,
)


class AnalyticalScoreRunner:
    """
    Builds the canonical Analytical Score from the
    AnalysisContext.

    The runner does not perform scientific analysis.

    It converts the already reconstructed musical
    information into a visualization-ready analytical
    representation.
    """

    def __init__(self) -> None:

        self._builder = (
            AnalyticalScoreBuilder()
        )

    def run(
        self,
        context: AnalysisContext,
    ) -> None:

        context.analytical_score = (
            self._builder.build(
                context,
            )
        )
