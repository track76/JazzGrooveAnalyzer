import matplotlib.figure

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
                time=0.0,
            ),
            VisualPoint(
                x=1.0,
                y=10.0,
                time=1.0,
            ),
        )
    )

    renderer = MatplotlibRenderer()

    figure = renderer.render(
        trajectory,
    )

    assert isinstance(
        figure,
        matplotlib.figure.Figure,
    )
