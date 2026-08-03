from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_style import (
    GraphicStyle,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_graphic_composition_full_validation():

    composition = GraphicComposition(
        elements=(
            LineElement(
                style=GraphicStyle(),
            ),
        ),
        style=GraphicStyle(),
        metadata={
            "purpose": "scientific_scene",
        },
    )

    assert composition.is_valid()
