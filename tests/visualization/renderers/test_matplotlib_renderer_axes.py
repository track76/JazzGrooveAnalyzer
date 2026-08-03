from matplotlib.figure import Figure

from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_renderer_produces_figure_with_axes():

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(),
        )
        .render()
    )

    assert isinstance(
        output.content,
        Figure,
    )

    assert len(
        output.content.axes
    ) > 0
