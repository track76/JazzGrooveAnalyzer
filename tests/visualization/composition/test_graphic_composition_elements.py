from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.line_element import (
    LineElement,
)


def test_graphic_composition_contains_elements():

    element = LineElement()

    composition = GraphicComposition(
        elements=(
            element,
        ),
    )

    assert composition.elements == (
        element,
    )
