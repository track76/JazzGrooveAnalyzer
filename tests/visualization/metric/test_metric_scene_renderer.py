from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)

from jga.visualization.graphic_element import (
    GraphicElement,
)

from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)


def test_metric_scene_can_be_rendered():

    scene = GraphicScene(
        compositions=(
            GraphicComposition(
                elements=(
                    GraphicElement(
                        element_type="metric_series",
                    ),
                ),
            ),
        ),
    )

    output = MatplotlibGraphicRenderer(
        scene=scene,
    ).render()

    assert output.content is not None
