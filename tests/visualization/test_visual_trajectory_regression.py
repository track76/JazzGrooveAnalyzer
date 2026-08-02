from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_complete_contract():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(
                x=0.0,
                y=0.0,
                time=10.0,
            ),
            VisualPoint(
                x=1.0,
                y=1.0,
                time=20.0,
            ),
            VisualPoint(
                x=2.0,
                y=2.0,
                time=30.0,
            ),
        ),
    )

    assert not trajectory.is_empty()

    assert trajectory.point_count() == 3

    assert trajectory.first_point().time == 10.0

    assert trajectory.last_point().time == 30.0

    assert trajectory.start_time() == 10.0

    assert trajectory.end_time() == 30.0

    assert trajectory.duration() == 20.0

    sliced = trajectory.slice(
        start_time=15.0,
        end_time=25.0,
    )

    assert sliced.point_count() == 1

    assert sliced.first_point().time == 20.0
