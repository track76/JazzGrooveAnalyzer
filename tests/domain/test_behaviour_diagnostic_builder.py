from jga.domain.services.behaviour_diagnostic_builder import (
    BehaviourDiagnosticBuilder,
)

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


def test_behaviour_diagnostic_builder():

    regions = StableRegionDetectionResult(
        events=(),
        evidences=(),
    )

    evidence = ScientificEvidenceCollection(
        evidences=(),
    )

    result = BehaviourDiagnosticBuilder().build(
        regions,
        evidence,
    )

    assert result.stable_regions == regions
    assert result.scientific_evidence == evidence
