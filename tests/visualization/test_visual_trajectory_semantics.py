from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_preserves_temporal_order():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=-5.0,
            ),
            VisualPoint(
                x=1.0,
                y=3.0,
            ),
            VisualPoint(
                x=2.0,
                y=8.0,
            ),
        )
    )

    assert trajectory.points[0].x == 0.0
    assert trajectory.points[1].x == 1.0
    assert trajectory.points[2].x == 2.0


def test_visual_trajectory_preserves_metric_evolution():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=-5.0,
            ),
            VisualPoint(
                x=1.0,
                y=3.0,
            ),
        )
    )

    assert trajectory.points[0].y == -5.0
    assert trajectory.points[1].y == 3.0
