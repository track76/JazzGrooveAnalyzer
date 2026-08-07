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

from jga.visualization.measure_block import (
    MeasureBlock,
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

        return self.render_measure_block(
            context,
            0,
            4,
        )

    def render_measure_block(
        self,
        context: AnalysisContext,
        start_measure: int,
        count: int,
    ):

        if context.analytical_score is None:
            raise ValueError(
                "AnalyticalScore required."
            )

        measures = (
            context.analytical_score.measures
        )

        if not measures:
            raise ValueError(
                "No measures available."
            )

        selected = measures[
            start_measure:
            start_measure + count
        ]

        if not selected:
            raise ValueError(
                "No measures selected."
            )

        return self._renderer.render(
            MeasureBlock(
                measures=tuple(selected)
            )
        )
