from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_reports_duration():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=0.0,
                time=12.5,
            ),
            VisualPoint(
                x=1.0,
                y=0.0,
                time=18.0,
            ),
            VisualPoint(
                x=2.0,
                y=0.0,
                time=25.5,
            ),
        ),
    )

    assert trajectory.duration() == 13.0
