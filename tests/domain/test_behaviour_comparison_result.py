from jga.domain.behaviour_comparison_result import (
    BehaviourComparisonResult,
)


def test_overall_match():

    result = BehaviourComparisonResult(

        physical_offset_match=True,

        metric_offset_match=True,

        internal_bpm_match=True,

        stability_match=True,

    )

    assert result.overall_match


def test_partial_match():

    result = BehaviourComparisonResult(

        physical_offset_match=True,

        metric_offset_match=False,

        internal_bpm_match=True,

        stability_match=True,

    )

    assert not result.overall_match

