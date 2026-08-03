from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_graphic_composition_accepts_valid_elements():

    composition = GraphicComposition(
        elements=(
            LineElement(),
        ),
    )

    assert composition.is_valid()
