from __future__ import annotations

from jga.domain.behaviour_space_relationship import (
    BehaviourSpaceRelationship,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)


class BehaviourSpaceRelationshipBuilder:
    """
    Builds BehaviourSpaceRelationship objects.

    Current implementation only validates
    structural coincidence.

    No geometric relationship calculation
    is performed.
    """

    def build(
        self,
        first: ScientificBehaviourSpace,
        second: ScientificBehaviourSpace,
    ) -> BehaviourSpaceRelationship:

        if (
            first.trajectory_count
            ==
            second.trajectory_count
        ):
            return (
                BehaviourSpaceRelationship.COINCIDENT
            )

        return (
            BehaviourSpaceRelationship.PARTIALLY_OVERLAPPING
        )
