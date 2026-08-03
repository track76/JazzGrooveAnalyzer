from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)


def test_metric_scene_contains_composition():

    composition = GraphicComposition(
        elements=(
            GraphicElement(
                element_type="metric_series",
            ),
        ),
    )

    scene = GraphicScene(
        compositions=(
            composition,
        ),
    )

    assert scene.compositions[0] is composition
