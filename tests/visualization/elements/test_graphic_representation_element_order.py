from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.materialized_plot import (
    MaterializedPlot,
)

from jga.visualization.line_element import (
    LineElement,
)

from jga.visualization.point_element import (
    PointElement,
)


def test_graphic_representation_preserves_element_order():

    line = LineElement()

    point = PointElement()

    representation = GraphicRepresentation(
        source_plot=MaterializedPlot(),
        elements=(
            line,
            point,
        ),
    )

    assert representation.elements[0] is line

    assert representation.elements[1] is point
