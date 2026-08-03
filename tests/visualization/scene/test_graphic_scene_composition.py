from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.graphic_composition import (
    GraphicComposition,
)


def test_graphic_scene_contains_compositions():

    composition = GraphicComposition()

    scene = GraphicScene(
        compositions=(
            composition,
        ),
    )

    assert scene.compositions == (
        composition,
    )
