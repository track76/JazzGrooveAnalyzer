
import pytest

from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)

from jga.domain.services.behaviour_evidence_aggregator import (
    BehaviourEvidenceAggregator,
)


def test_behaviour_evidence_aggregator():

    evidences = (
        BehaviourComparisonEvidence(
            physical_offset_delta_ms=2.0,
            metric_offset_delta=0.2,
            internal_bpm_delta=1.0,
            stability_delta=-0.2,
        ),
        BehaviourComparisonEvidence(
            physical_offset_delta_ms=4.0,
            metric_offset_delta=0.4,
            internal_bpm_delta=3.0,
            stability_delta=0.2,
        ),
    )

    result = (
        BehaviourEvidenceAggregator()
        .aggregate(evidences)
    )

    assert result.comparison_count == 2

    assert (
        result.mean_physical_offset_delta_ms
        == 3.0
    )

    assert (
        result.mean_metric_offset_delta
        == pytest.approx(0.3)
    )

