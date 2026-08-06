"""
=========================================================
Jazz Groove Analyzer (JGA)

Analytical Groove Score Renderer Runner

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext

from jga.visualization.renderers.analytical_groove_score_v3_renderer import (
    AnalyticalGrooveScoreV3Renderer,
)


class AnalyticalGrooveScoreRendererRunner:
    """
    Renders the Analytical Groove Score.

    Uses only already reconstructed analytical data.
    No scientific computation is performed.
    """

    def __init__(self) -> None:

        self._renderer = (
            AnalyticalGrooveScoreV3Renderer()
        )

    def render_first_measure(
        self,
        context: AnalysisContext,
    ):

        if context.analytical_score is None:
            raise ValueError(
                "AnalyticalScore required."
            )

        if not context.analytical_score.measures:
            raise ValueError(
                "No measures available."
            )

        return self._renderer.render(
            context.analytical_score.measures[0]
        )
