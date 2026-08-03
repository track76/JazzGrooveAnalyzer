from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_scientific_graphic_builder_creates_elements():

    representation = (
        ScientificGraphicBuilder()
        .build(
            MaterializedPlot()
        )
    )

    assert len(
        representation.elements
    ) > 0

    assert isinstance(
        representation.elements[0],
        GraphicElement,
    )
