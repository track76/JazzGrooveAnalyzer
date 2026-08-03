from jga.visualization.graphic_element import (
    GraphicElement,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_element_accepts_style():

    style = GraphicStyle()

    element = GraphicElement(
        style=style,
    )

    assert element.style is style
