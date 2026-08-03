from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_style_exposes_type():

    style = GraphicStyle(
        style_type="scientific",
    )

    assert style.style_type == "scientific"
