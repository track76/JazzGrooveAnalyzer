from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)


def test_graphic_renderer_exists():

    renderer = GraphicRenderer()

    assert renderer is not None
