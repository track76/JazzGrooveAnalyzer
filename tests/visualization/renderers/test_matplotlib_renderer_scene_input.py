from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_matplotlib_renderer_accepts_scene():

    scene = GraphicScene()

    renderer = MatplotlibGraphicRenderer(
        scene=scene,
    )

    assert renderer.scene is scene
