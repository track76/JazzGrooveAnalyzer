from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.rendered_output import (
    RenderedOutput,
)


def test_renderer_returns_rendered_output():

    renderer = GraphicRenderer(
        scene=GraphicScene(),
    )

    output = renderer.render()

    assert isinstance(
        output,
        RenderedOutput,
    )
