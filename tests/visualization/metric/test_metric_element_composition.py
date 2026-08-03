from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_metric_element_can_be_composed():

    element = GraphicElement(
        element_type="metric_series",
    )

    composition = GraphicComposition(
        elements=(
            element,
        ),
    )

    assert composition.elements[0] is element
