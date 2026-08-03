from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_scene_accepts_valid_compositions():

    scene = GraphicScene(
        compositions=(
            GraphicComposition(),
        ),
    )

    assert scene.is_valid()
