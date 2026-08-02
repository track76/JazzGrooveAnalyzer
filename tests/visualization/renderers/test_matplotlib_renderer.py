from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)

from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_matplotlib_renderer_creates_figure():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=-5.0,
            ),
            VisualPoint(
                x=1.0,
                y=10.0,
            ),
        )
    )

    figure = (
        MatplotlibRenderer()
        .render(trajectory)
    )

    assert figure is not None
