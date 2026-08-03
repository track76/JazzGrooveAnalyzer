from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_matplotlib_renderer_validates_scene():

    renderer = MatplotlibGraphicRenderer(
        scene=GraphicScene(),
    )

    assert renderer.is_valid()
