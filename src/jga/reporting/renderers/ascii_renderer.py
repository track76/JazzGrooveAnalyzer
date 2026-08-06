"""
Compatibility adapter for the legacy Reporting layer.

The canonical ASCII renderer lives in the Visualization layer.
"""

from jga.visualization.analytical_score import (
    AnalyticalScore,
)

from jga.visualization.ascii_analytical_score_renderer import (
    AsciiAnalyticalScoreRenderer,
)


class AnalyticalScoreAsciiRenderer:
    """
    Compatibility adapter.

    Delegates rendering to the canonical
    Visualization ASCII renderer.
    """

    def __init__(self):

        self._renderer = (
            AsciiAnalyticalScoreRenderer()
        )

    def render(
        self,
        score: AnalyticalScore,
    ) -> str:

        return self._renderer.render(
            score,
        )
