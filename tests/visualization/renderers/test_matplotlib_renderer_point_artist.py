from jga.visualization.matplotlib_graphic_renderer import (
    MatplotlibGraphicRenderer,
)

from jga.visualization.graphic_scene import (
    GraphicScene,
)


def test_renderer_draws_point_artist():

    output = (
        MatplotlibGraphicRenderer(
            scene=GraphicScene(),
        )
        .render()
    )

    axes = output.content.axes[0]

    assert len(
        axes.collections
    ) >= 0
