from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_matplotlib_renderer_produces_content():

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(),
        )
        .render()
    )

    assert output.content is not None
