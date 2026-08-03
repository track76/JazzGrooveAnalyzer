from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_renderer_exposes_output():

    renderer = GraphicRenderer(
        scene=GraphicScene(),
    )

    assert renderer.render() is not None
