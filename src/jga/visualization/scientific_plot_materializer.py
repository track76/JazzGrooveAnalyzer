"""
Scientific Plot Materializer.

Responsible for converting plot
representations into materialized plots.
"""

from jga.visualization.plot_representation import (
    PlotRepresentation,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


class ScientificPlotMaterializer:
    """
    Scientific plot materializer.
    """

    def materialize(
        self,
        representation: PlotRepresentation,
    ) -> MaterializedPlot:
        """
        Materializes a plot representation
        into a concrete plot structure.
        """

        return MaterializedPlot(
            source_representation=representation,
            metadata={},
        )
