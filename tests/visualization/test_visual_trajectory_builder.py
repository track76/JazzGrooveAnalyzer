from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory_builder import (
    VisualTrajectoryBuilder,
)


def test_builder_creates_visual_trajectory():

    points = (
        VisualPoint(
            x=0.0,
            y=0.0,
        ),
        VisualPoint(
            x=1.0,
            y=2.0,
        ),
    )

    trajectory = (
        VisualTrajectoryBuilder()
        .build(points)
    )

    assert trajectory.points == points
