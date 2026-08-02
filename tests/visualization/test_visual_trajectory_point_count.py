from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_reports_point_count():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=0.0,
                time=0.0,
            ),
            VisualPoint(
                x=1.0,
                y=1.0,
                time=1.0,
            ),
            VisualPoint(
                x=2.0,
                y=2.0,
                time=2.0,
            ),
        ),
    )

    assert trajectory.point_count() == 3
