from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_scientific_graphic_builder_populates_element_metadata():

    representation = (
        ScientificGraphicBuilder()
        .build(
            MaterializedPlot()
        )
    )

    assert all(
        element.metadata
        for element in representation.elements
    )
