from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.geometric_point import GeometricPoint
from jga.geometry.scientific_coordinate import ScientificCoordinate


def build_point():

    return GeometricPoint(
        coordinates=[
            ScientificCoordinate(
                name="metric_offset",
                value=0.0,
                unit="beats",
            )
        ]
    )


def test_empty():

    trajectory = BehaviourTrajectory()

    assert trajectory.is_empty
    assert trajectory.point_count == 0
    assert trajectory.first_point is None
    assert trajectory.last_point is None


def test_iteration():

    point = build_point()

    trajectory = BehaviourTrajectory(
        points=[point],
    )

    assert list(trajectory) == [point]

