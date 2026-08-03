"""
Scientific Graphic Builder.

Responsible for creating abstract
graphic representations.
"""

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)


class ScientificGraphicBuilder:
    """
    Scientific graphic builder.
    """

    def build(
        self,
        plot: MaterializedPlot,
    ) -> GraphicRepresentation:
        """
        Builds a graphic representation
        from a materialized plot.
        """

        return GraphicRepresentation(
            source_plot=plot,
            metadata={},
        )
