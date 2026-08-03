from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_graphic_scene_exposes_metadata():

    scene = GraphicScene(
        metadata={
            "purpose": "scientific_visualization",
        },
    )

    assert scene.metadata == {
        "purpose": "scientific_visualization",
    }
