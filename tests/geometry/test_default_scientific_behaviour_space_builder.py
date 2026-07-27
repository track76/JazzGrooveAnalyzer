from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.builders.default_scientific_behaviour_space_builder import (
    DefaultScientificBehaviourSpaceBuilder,
)
from jga.geometry.geometric_point import GeometricPoint
from jga.geometry.scientific_behaviour_space import ScientificBehaviourSpace
from jga.geometry.scientific_coordinate import ScientificCoordinate
from jga.geometry.scientific_geometric_plane import ScientificGeometricPlane


def test_build():

    plane = ScientificGeometricPlane(
        points=[
            GeometricPoint(
                coordinates=[
                    ScientificCoordinate(
                        name="offset",
                        value=0.0,
                        unit="beats",
                    )
                ]
            )
        ]
    )

    builder = DefaultScientificBehaviourSpaceBuilder()

    space = builder.build(plane)

    assert isinstance(space, ScientificBehaviourSpace)
    assert isinstance(space.first_trajectory, BehaviourTrajectory)
    assert space.trajectory_count == 1
    assert space.first_trajectory.point_count == 1

