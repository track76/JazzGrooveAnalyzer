from jga.visualization.line_element import (
    LineElement,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_line_element_accepts_style():

    style = GraphicStyle()

    element = LineElement(
        style=style,
    )

    assert element.style is style
