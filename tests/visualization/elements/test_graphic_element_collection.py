from jga.visualization.graphic_representation import (
    GraphicRepresentation,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_graphic_representation_contains_elements():

    element = GraphicElement()

    representation = GraphicRepresentation(
        elements=(element,),
    )

    assert element in representation.elements
