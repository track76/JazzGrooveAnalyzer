from __future__ import annotations

from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.scientific_behaviour_space import ScientificBehaviourSpace
from jga.geometry.scientific_geometric_plane import ScientificGeometricPlane
from jga.interfaces.geometry.scientific_behaviour_space_builder import (
    ScientificBehaviourSpaceBuilder,
)


class DefaultScientificBehaviourSpaceBuilder(
    ScientificBehaviourSpaceBuilder
):

    def build(
        self,
        plane: ScientificGeometricPlane,
    ) -> ScientificBehaviourSpace:

        trajectory = BehaviourTrajectory(
            points=list(plane.points),
        )

        return ScientificBehaviourSpace(
            trajectories=[trajectory],
        )

