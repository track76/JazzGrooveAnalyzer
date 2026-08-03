from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_matplotlib_renderer_preserves_scene_metadata():

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(
                metadata={
                    "purpose": "scientific_scene",
                },
            ),
        )
        .render()
    )

    assert output.metadata["renderer"] == "matplotlib"
