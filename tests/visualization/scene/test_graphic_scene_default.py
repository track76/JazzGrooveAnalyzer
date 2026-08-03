from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_scene_default_state():

    scene = GraphicScene()

    assert scene.compositions == ()

    assert scene.metadata == {}

    assert scene.is_valid()
