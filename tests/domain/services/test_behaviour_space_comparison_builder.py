from jga.domain.behaviour_space_comparison import (
    BehaviourSpaceComparison,
)

from jga.domain.services.behaviour_space_comparison_builder import (
    BehaviourSpaceComparisonBuilder,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


def test_comparison_detects_compatible_spaces():

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
        BehaviourSpaceComparisonBuilder()
        .build(first, second)
    )

    assert isinstance(
        result,
        BehaviourSpaceComparison,
    )

    assert result.comparable


def test_comparison_detects_incompatible_spaces():

    first = ScientificBehaviourSpace(
        trajectories=[]
    )

    second = ScientificBehaviourSpace(
        trajectories=[
            BehaviourTrajectory()
        ]
    )

    result = (
        BehaviourSpaceComparisonBuilder()
        .build(first, second)
    )

    assert not result.comparable
