from jga.visualization.scientific_graphic_builder import (
    ScientificGraphicBuilder,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_scientific_graphic_builder_populates_line_geometry():

    representation = (
        ScientificGraphicBuilder()
        .build(
            MaterializedPlot()
        )
    )

    line = representation.elements[0]

    assert isinstance(
        line,
        LineElement,
    )

    assert len(
        line.points
    ) > 0
