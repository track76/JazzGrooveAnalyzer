from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_scene_is_valid():

    scene = GraphicScene()

    assert scene.is_valid()
