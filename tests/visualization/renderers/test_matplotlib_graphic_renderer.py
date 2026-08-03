from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)


def test_matplotlib_graphic_renderer_exists():

    renderer = MatplotlibGraphicRenderer()

    assert renderer is not None
