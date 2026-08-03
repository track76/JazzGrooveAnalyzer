from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_exists():

    style = GraphicStyle()

    assert style is not None
