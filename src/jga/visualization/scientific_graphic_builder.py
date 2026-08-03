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

from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)

from jga.visualization.line_element import (
    LineElement,
)

from jga.visualization.point_element import (
    PointElement,
)


class ScientificGraphicBuilder:
    """
    Scientific graphic builder.
    """

    def build(
        self,
        plot: MaterializedPlot,
    ) -> GraphicRepresentation:

        style = GraphicStyle()

        return GraphicRepresentation(
            source_plot=plot,
            metadata={},
            elements=(
                LineElement(
                    points=(
                        (0.0, 0.0),
                        (1.0, 1.0),
                    ),
                    metadata={
                        "role": "trajectory",
                    },
                    style=style,
                ),
                PointElement(
                    position=(
                        0.0,
                        0.0,
                    ),
                    metadata={
                        "role": "marker",
                    },
                    style=style,
                ),
            ),
        )

    def compose(
        self,
        plot: MaterializedPlot,
    ) -> GraphicComposition:

        representation = self.build(plot)

        return GraphicComposition(
            elements=representation.elements,
            metadata=representation.metadata,
            style=GraphicStyle(),
        )
