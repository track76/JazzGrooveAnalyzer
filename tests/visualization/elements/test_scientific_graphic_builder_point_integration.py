from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.point_element import (
    PointElement,
)


def test_scientific_graphic_builder_creates_point_element():

    representation = (
        ScientificGraphicBuilder()
        .build(
            MaterializedPlot()
        )
    )

    assert any(
        isinstance(
            element,
            PointElement,
        )
        for element in representation.elements
    )
