from jga.visualization.graphic_element import (
    GraphicElement,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_element_accepts_valid_style():

    element = GraphicElement(
        style=GraphicStyle(),
    )

    assert element.style.is_valid()
