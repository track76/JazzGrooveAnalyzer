from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_slice():

    trajectory = VisualTrajectory(
        points=(
            VisualPoint(x=0.0, y=0.0, time=0.0),
            VisualPoint(x=1.0, y=0.0, time=1.0),
            VisualPoint(x=2.0, y=0.0, time=2.0),
            VisualPoint(x=3.0, y=0.0, time=3.0),
            VisualPoint(x=4.0, y=0.0, time=4.0),
        ),
    )

    sliced = trajectory.slice(
        start_time=1.5,
        end_time=3.5,
    )

    assert sliced.point_count() == 2

    assert sliced.start_time() == 2.0

    assert sliced.end_time() == 3.0
