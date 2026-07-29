from jga.domain.behaviour_space_relationship import (
    BehaviourSpaceRelationship,
)

from jga.domain.services.behaviour_space_relationship_builder import (
    BehaviourSpaceRelationshipBuilder,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)


def test_returns_coincident_for_same_structure():

    first = ScientificBehaviourSpace(
        trajectories=[
            BehaviourTrajectory()
        ]
    )

    second = ScientificBehaviourSpace(
        trajectories=[
            BehaviourTrajectory()
        ]
    )

    result = (
        BehaviourSpaceRelationshipBuilder()
        .build(first, second)
    )

    assert (
        result
        ==
        BehaviourSpaceRelationship.COINCIDENT
    )


def test_returns_non_coincident_for_different_structure():

    first = ScientificBehaviourSpace(
        trajectories=[]
    )

    second = ScientificBehaviourSpace(
        trajectories=[
            BehaviourTrajectory()
        ]
    )

    result = (
        BehaviourSpaceRelationshipBuilder()
        .build(first, second)
    )

    assert (
        result
        ==
        BehaviourSpaceRelationship.PARTIALLY_OVERLAPPING
    )
