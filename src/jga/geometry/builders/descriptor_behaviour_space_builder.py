from __future__ import annotations

from jga.domain.descriptor_set import DescriptorSet

from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.geometric_point import GeometricPoint
from jga.geometry.scientific_behaviour_space import ScientificBehaviourSpace

from jga.geometry.builders.descriptor_space_projection_builder import (
    DescriptorSpaceProjectionBuilder,
)

from jga.geometry.builders.scientific_geometric_point_builder import (
    ScientificGeometricPointBuilder,
)


class DescriptorBehaviourSpaceBuilder:
    """
    Builds a ScientificBehaviourSpace from
    validated Behaviour Descriptors.

    No analytical transformation is performed.
    Descriptor values become scientific coordinates.
    """

    def __init__(self) -> None:

        self._projection_builder = (
            DescriptorSpaceProjectionBuilder()
        )

        self._point_builder = (
            ScientificGeometricPointBuilder()
        )

    def build(
        self,
        descriptor_set: DescriptorSet,
    ) -> ScientificBehaviourSpace:

        projection = (
            self._projection_builder.build(
                descriptor_set
            )
        )

        point = (
            self._point_builder.build(
                projection
            )
        )

        trajectory = BehaviourTrajectory(
            points=[point],
        )

        return ScientificBehaviourSpace(
            trajectories=[trajectory],
        )
