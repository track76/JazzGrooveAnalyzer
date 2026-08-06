"""
=========================================================
Jazz Groove Analyzer (JGA)

Analytical Groove Score PNG Exporter Runner

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext

from jga.visualization.exporters.figure_exporter import (
    FigureExporter,
)

from jga.runtime.engines.analytical_groove_score_renderer_runner import (
    AnalyticalGrooveScoreRendererRunner,
)


class AnalyticalGrooveScorePngExporterRunner:
    """
    Generates PNG output from the Analytical Groove Score.

    Rendering and persistence remain separated.
    """

    def __init__(self) -> None:

        self._renderer = (
            AnalyticalGrooveScoreRendererRunner()
        )

        self._exporter = (
            FigureExporter()
        )

    def export(
        self,
        context: AnalysisContext,
        destination: str,
    ) -> None:

        figure = (
            self._renderer
            .render_first_measure(
                context,
            )
        )

        self._exporter.export(
            figure,
            destination,
        )
