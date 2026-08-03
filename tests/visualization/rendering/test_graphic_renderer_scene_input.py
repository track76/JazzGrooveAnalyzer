from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_renderer_accepts_scene():

    scene = GraphicScene()

    renderer = GraphicRenderer(
        scene=scene,
    )

    assert renderer.scene is scene
