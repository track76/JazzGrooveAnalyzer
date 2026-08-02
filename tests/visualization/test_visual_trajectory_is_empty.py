from jga.visualization.visual_point import (
    VisualPoint,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


def test_visual_trajectory_is_empty():

    assert (
        VisualTrajectory()
        .is_empty()
    )

    assert not (
        VisualTrajectory(
            points=(
                VisualPoint(
                    x=0.0,
                    y=0.0,
                    time=0.0,
                ),
            ),
        )
        .is_empty()
    )
