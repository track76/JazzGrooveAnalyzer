from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_renderer_propagates_scene_metadata():

    scene = GraphicScene(
        metadata={
            "purpose": "scientific_scene",
        },
    )

    output = GraphicRenderer(
        scene=scene,
    ).render()

    assert output.metadata == {
        "purpose": "scientific_scene",
    }
