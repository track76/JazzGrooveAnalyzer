from jga.visualization.visual_point import (
    VisualPoint,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visualization_represents_observable_metric_evolution():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=-2.0,
                time=0.0,
            ),
            VisualPoint(
                x=1.0,
                y=1.0,
                time=1.0,
            ),
            VisualPoint(
                x=2.0,
                y=-1.0,
                time=2.0,
            ),
        )
    )

    assert len(trajectory.points) == 3

    assert trajectory.points[0].y == -2.0
    assert trajectory.points[1].y == 1.0
    assert trajectory.points[2].y == -1.0


def test_visualization_does_not_assign_musical_judgement():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=0.0,
                time=0.0,
            ),
        )
    )

    assert trajectory.points[0].y == 0.0
