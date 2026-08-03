from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_graphic_element_exposes_type():

    element = GraphicElement(
        element_type="generic",
    )

    assert element.element_type == "generic"
