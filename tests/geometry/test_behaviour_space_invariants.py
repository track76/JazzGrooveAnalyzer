from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.geometric_point import GeometricPoint
from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)
from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


def build_point(index: int):

    return GeometricPoint(
        coordinates=[
            ScientificCoordinate(
                name="offset",
                value=float(index),
                unit="beats",
            )
        ]
    )


def test_cardinality():

    trajectory = BehaviourTrajectory(
        points=[
            build_point(0),
            build_point(1),
            build_point(2),
        ]
    )

    space = ScientificBehaviourSpace(
        trajectories=[trajectory],
    )

    assert trajectory.point_count == 3


def test_temporal_order():

    trajectory = BehaviourTrajectory(
        points=[
            build_point(0),
            build_point(1),
            build_point(2),
        ]
    )

    assert (
        trajectory.first_point.coordinates[0].value
        == 0.0
    )

    assert (
        trajectory.last_point.coordinates[0].value
        == 2.0
    )


def test_iteration():

    trajectory = BehaviourTrajectory(
        points=[
            build_point(0),
            build_point(1),
        ]
    )

    space = ScientificBehaviourSpace(
        trajectories=[trajectory],
    )

    assert list(space)[0] is trajectory

