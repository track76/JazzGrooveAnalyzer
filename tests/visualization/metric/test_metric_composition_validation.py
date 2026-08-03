from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_metric_composition_is_valid():

    composition = GraphicComposition(
        elements=(
            GraphicElement(
                element_type="metric_series",
            ),
        ),
    )

    assert composition.is_valid()
