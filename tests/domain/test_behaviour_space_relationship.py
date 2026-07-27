from jga.domain.behaviour_space_relationship import (
    BehaviourSpaceRelationship,
)


def test_enum():

    assert (
        BehaviourSpaceRelationship.COINCIDENT.value
        == "coincident"
    )

    assert (
        BehaviourSpaceRelationship.DIVERGENT.value
        == "divergent"
    )

