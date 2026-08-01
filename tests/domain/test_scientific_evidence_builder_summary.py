
from jga.domain.behaviour_evidence_summary import (
    BehaviourEvidenceSummary,
)

from jga.domain.services.scientific_evidence_builder import (
    ScientificEvidenceBuilder,
)


def test_scientific_evidence_builder_from_summary():

    summary = BehaviourEvidenceSummary(
        comparison_count=100,
        mean_physical_offset_delta_ms=0.5,
        mean_metric_offset_delta=0.1,
        mean_internal_bpm_delta=1.0,
        mean_stability_delta=-0.05,
    )

    result = (
        ScientificEvidenceBuilder()
        .build_from_summary(summary)
    )

    assert len(result.evidences) == 4

    names = {
        evidence.name
        for evidence in result.evidences
    }

    assert names == {
        "physical_offset",
        "metric_offset",
        "internal_bpm",
        "stability",
    }

    values = {
        evidence.name: evidence.value
        for evidence in result.evidences
    }

    assert (
        values["physical_offset"]
        == 0.5
    )

    assert (
        values["metric_offset"]
        == 0.1
    )

