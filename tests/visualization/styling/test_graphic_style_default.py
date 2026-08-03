from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_default_metadata_is_empty():

    style = GraphicStyle()

    assert style.metadata == {}

    assert style.is_valid()
