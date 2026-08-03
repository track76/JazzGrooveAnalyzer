from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_graphic_representation_validates_elements():

    representation = GraphicRepresentation(
        source_plot=MaterializedPlot(),
        elements=(
            GraphicElement(
                element_type="generic",
            ),
        ),
    )

    assert representation.is_valid()
