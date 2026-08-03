from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_graphic_element_exposes_metadata():

    element = GraphicElement(
        metadata={
            "role": "generic",
        },
    )

    assert element.metadata == {
        "role": "generic",
    }
