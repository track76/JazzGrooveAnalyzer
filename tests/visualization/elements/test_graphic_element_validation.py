from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_graphic_element_is_valid():

    element = GraphicElement(
        element_type="generic",
    )

    assert element.is_valid()
