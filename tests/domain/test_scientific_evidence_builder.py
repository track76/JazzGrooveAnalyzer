from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)

from jga.domain.services.scientific_evidence_builder import (
    ScientificEvidenceBuilder,
)


def test_scientific_evidence_builder():

    source = BehaviourComparisonEvidence(
        physical_offset_delta_ms=2.0,
        metric_offset_delta=0.1,
        internal_bpm_delta=1.0,
        stability_delta=-0.1,
    )

    result = ScientificEvidenceBuilder().build(
        (source,)
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
