from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_composition_accepts_style():

    style = GraphicStyle()

    composition = GraphicComposition(
        style=style,
    )

    assert composition.style is style
