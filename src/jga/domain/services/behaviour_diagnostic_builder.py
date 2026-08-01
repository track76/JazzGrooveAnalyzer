from jga.domain.behaviour_diagnostic_result import (
    BehaviourDiagnosticResult,
)

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


class BehaviourDiagnosticBuilder:
    """
    Builds BehaviourDiagnosticResult.

    This service only composes validated results.
    No scientific interpretation is performed.
    """

    def build(
        self,
        stable_regions: StableRegionDetectionResult,
        scientific_evidence: ScientificEvidenceCollection,
    ) -> BehaviourDiagnosticResult:

        return BehaviourDiagnosticResult(
            stable_regions=stable_regions,
            scientific_evidence=scientific_evidence,
        )
