from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_default_type():

    style = GraphicStyle()

    assert style.style_type == "default"

    assert style.metadata == {}

    assert style.is_valid()
