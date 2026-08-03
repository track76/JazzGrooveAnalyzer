from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_graphic_representation_requires_valid_elements():

    representation = GraphicRepresentation(
        source_plot=MaterializedPlot(),
        elements=(
            GraphicElement(
                element_type="generic",
            ),
        ),
    )

    assert representation.is_valid()
