
from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.domain.services.default_behaviour_state_segmenter import (
    DefaultBehaviourStateSegmenter,
)


def create_point(value: float) -> GeometricPoint:

    return GeometricPoint(
        coordinates=(
            ScientificCoordinate(
                name="x",
                value=value,
                unit="a.u.",
            ),
        )
    )


def test_empty_trajectory_returns_no_states():

    trajectory = BehaviourTrajectory()

    result = (
        DefaultBehaviourStateSegmenter()
        .segment(trajectory)
    )

    assert result == ()


def test_trajectory_is_preserved_as_single_state():

    trajectory = BehaviourTrajectory(
        points=[
            create_point(0.0),
            create_point(1.0),
            create_point(2.0),
        ]
    )

    result = (
        DefaultBehaviourStateSegmenter()
        .segment(trajectory)
    )

    assert len(result) == 1

    state = result[0]

    assert state.start_index == 0
    assert state.end_index == 2
    assert state.duration == 3
    assert state.trajectory == trajectory

