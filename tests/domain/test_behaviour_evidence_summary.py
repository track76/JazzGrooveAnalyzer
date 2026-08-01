
from jga.domain.behaviour_evidence_summary import (
    BehaviourEvidenceSummary,
)


def test_behaviour_evidence_summary():

    summary = BehaviourEvidenceSummary(
        comparison_count=10,
        mean_physical_offset_delta_ms=0.0,
        mean_metric_offset_delta=0.0,
        mean_internal_bpm_delta=0.0,
        mean_stability_delta=0.0,
    )

    assert summary.comparison_count == 10

    assert summary.is_stable is True

