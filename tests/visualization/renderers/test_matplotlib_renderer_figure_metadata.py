from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_renderer_marks_figure_output():

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(),
        )
        .render()
    )

    assert output.metadata["renderer"] == "matplotlib"

    assert output.metadata["type"] == "figure"
