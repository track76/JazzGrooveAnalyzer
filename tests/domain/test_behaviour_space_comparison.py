from jga.domain.behaviour_space_comparison import (
    BehaviourSpaceComparison,
)


def test_creation():

    comparison = BehaviourSpaceComparison(
        comparable=True,
        reason="compatible",
    )

    assert comparison.comparable
    assert comparison.reason == "compatible"

