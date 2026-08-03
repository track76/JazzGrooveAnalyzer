from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.rendered_output import (
    RenderedOutput,
)


def test_matplotlib_renderer_returns_output():

    renderer = MatplotlibGraphicRenderer(
        scene=GraphicScene(),
    )

    output = renderer.render()

    assert isinstance(
        output,
        RenderedOutput,
    )
