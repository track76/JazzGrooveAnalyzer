from jga.visualization.ascii_renderer import (
    ASCIIRenderer,
)

from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_ascii_renderer_outputs_points():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=1.0,
            ),
            VisualPoint(
                x=2.0,
                y=3.0,
            ),
        )
    )

    output = (
        ASCIIRenderer()
        .render(trajectory)
    )

    assert output == (
        "(0.0,1.0)\n"
        "(2.0,3.0)"
    )
