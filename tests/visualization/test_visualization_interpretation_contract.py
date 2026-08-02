from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.visual_point import (
    VisualPoint,
)


def test_visualization_represents_observable_metric_evolution():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=-2.0,
            ),
            VisualPoint(
                x=1.0,
                y=1.0,
            ),
            VisualPoint(
                x=2.0,
                y=-1.0,
            ),
        )
    )

    values = tuple(
        point.y
        for point in trajectory.points
    )

    assert values == (
        -2.0,
        1.0,
        -1.0,
    )


def test_visualization_does_not_assign_musical_judgement():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=0.0,
            ),
        )
    )

    assert not hasattr(
        trajectory,
        "musical_quality",
    )

    assert not hasattr(
        trajectory,
        "groove_score",
    )
