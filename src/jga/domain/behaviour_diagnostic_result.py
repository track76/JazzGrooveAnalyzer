from dataclasses import dataclass

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.domain.scientific_evidence_collection import (
    ScientificEvidenceCollection,
)


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourDiagnosticResult:
    """
    Result of Behaviour Diagnostics.

    Preserves detected regions and scientific evidence.
    """

    stable_regions: StableRegionDetectionResult

    scientific_evidence: ScientificEvidenceCollection
