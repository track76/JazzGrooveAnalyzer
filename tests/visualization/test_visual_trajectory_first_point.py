from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_returns_first_point():

    first = VisualPoint(
        x=0.0,
        y=1.0,
        time=2.0,
    )

    trajectory = VisualTrajectory(
        points=(
            first,
            VisualPoint(
                x=3.0,
                y=4.0,
                time=5.0,
            ),
        ),
    )

    assert trajectory.first_point() is first
