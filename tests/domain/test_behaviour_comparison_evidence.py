from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)


def test_behaviour_comparison_evidence_creation():

    evidence = BehaviourComparisonEvidence(
        physical_offset_delta_ms=2.0,
        metric_offset_delta=0.1,
        internal_bpm_delta=0.5,
        stability_delta=0.02,
    )

    assert evidence.physical_offset_delta_ms == 2.0
    assert evidence.metric_offset_delta == 0.1
    assert evidence.internal_bpm_delta == 0.5
    assert evidence.stability_delta == 0.02
