"""
=========================================================
Jazz Groove Analyzer (JGA)

Figure Exporter

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from pathlib import Path

from matplotlib.figure import Figure


class FigureExporter:
    """
    Exports a matplotlib Figure.

    The renderer creates the Figure.
    The exporter persists it.
    """

    def export(
        self,
        figure: Figure,
        destination: str,
    ) -> None:

        path = Path(destination)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        figure.savefig(
            path,
            dpi=300,
            bbox_inches="tight",
        )
