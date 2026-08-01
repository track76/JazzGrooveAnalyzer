from jga.domain.behaviour_diagnostic_result import (
    BehaviourDiagnosticResult,
)

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


def test_behaviour_diagnostic_result():

    result = BehaviourDiagnosticResult(
        stable_regions=StableRegionDetectionResult(
            events=(),
            evidences=(),
        ),
        scientific_evidence=ScientificEvidenceCollection(
            evidences=(),
        ),
    )

    assert result.stable_regions.events == ()
    assert result.scientific_evidence.evidences == ()
