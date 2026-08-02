from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_preserves_points():

    point_a = VisualPoint(
        x=0.0,
        y=0.0,
    )

    point_b = VisualPoint(
        x=1.0,
        y=1.0,
    )

    trajectory = VisualTrajectory(
        points=(
            point_a,
            point_b,
        )
    )

    assert trajectory.points == (
        point_a,
        point_b,
    )


def test_visual_trajectory_is_immutable():

    trajectory = VisualTrajectory()

    try:
        trajectory.points = ()
        assert False
    except Exception:
        assert True
