from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_graphic_representation_requires_valid_element_styles():

    representation = GraphicRepresentation(
        source_plot=MaterializedPlot(),
        elements=(
            LineElement(),
        ),
    )

    assert representation.is_valid()
