from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)


def test_graphic_composition_style_is_valid():

    composition = GraphicComposition(
        style=GraphicStyle(),
    )

    assert composition.style.is_valid()
