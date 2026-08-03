from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_is_valid():

    style = GraphicStyle()

    assert style.is_valid()
