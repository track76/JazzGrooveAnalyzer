from jga.visualization.visual_point import (
    VisualPoint,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)
from jga.visualization.visual_trajectory_builder import (
    VisualTrajectoryBuilder,
)


def test_builder_creates_visual_trajectory():

    points = (
        VisualPoint(
            x=0.0,
            y=0.0,
            time=0.0,
        ),
        VisualPoint(
            x=1.0,
            y=2.0,
            time=1.0,
        ),
    )

    trajectory = (
        VisualTrajectoryBuilder()
        .build(points)
    )

    assert isinstance(
        trajectory,
        VisualTrajectory,
    )

    assert trajectory.points == points
