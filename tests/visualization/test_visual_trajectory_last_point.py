from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_returns_last_point():

    last = VisualPoint(
        x=3.0,
        y=4.0,
        time=5.0,
    )

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=1.0,
                time=2.0,
            ),
            last,
        ),
    )

    assert trajectory.last_point() is last
