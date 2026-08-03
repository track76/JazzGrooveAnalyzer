from jga.visualization.point_element import (
    PointElement,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_point_element_accepts_style():

    style = GraphicStyle()

    element = PointElement(
        style=style,
    )

    assert element.style is style
