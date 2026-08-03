from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_scene_exists():

    scene = GraphicScene()

    assert scene is not None
