from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)


def test_matplotlib_renderer_is_graphic_renderer():

    renderer = MatplotlibGraphicRenderer()

    assert isinstance(
        renderer,
        GraphicRenderer,
    )
