from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.line_element import (
    LineElement,
)

from jga.visualization.point_element import (
    PointElement,
)


def test_graphic_composition_preserves_element_order():

    line = LineElement()

    point = PointElement()

    composition = GraphicComposition(
        elements=(
            line,
            point,
        ),
    )

    assert composition.elements[0] is line
    assert composition.elements[1] is point
