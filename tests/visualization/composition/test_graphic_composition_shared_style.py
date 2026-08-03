from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_composition_can_share_style():

    style = GraphicStyle()

    composition = GraphicComposition(
        style=style,
    )

    assert composition.style is style
