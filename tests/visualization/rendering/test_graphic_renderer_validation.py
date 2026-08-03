from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)


def test_graphic_renderer_is_valid():

    renderer = GraphicRenderer()

    assert renderer.is_valid()
