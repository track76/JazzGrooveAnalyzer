from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.domain.stable_region_detection_result import (
    StableRegionDetectionResult,
)

from jga.observation.stable_region_detector import (
    StableRegionDetector,
)

from jga.domain.services.scientific_evidence_builder import (
    ScientificEvidenceBuilder,
)

from jga.domain.services.behaviour_diagnostic_builder import (
    BehaviourDiagnosticBuilder,
)


class DefaultBehaviourDiagnostics:
    """
    Behaviour Diagnostics coordinator.

    Each detector analyses one specific
    behavioural phenomenon.
    """

    def __init__(self):

        self._stable_detector = (
            StableRegionDetector()
        )

        self._evidence_builder = (
            ScientificEvidenceBuilder()
        )

        self._diagnostic_builder = (
            BehaviourDiagnosticBuilder()
        )

    def analyze(
        self,
        frames: tuple[
            BehaviourObservationFrame,
            ...
        ],
    ) -> StableRegionDetectionResult:

        stable_regions = (
            self._stable_detector.detect(
                frames,
            )
        )

        evidence = (
            self._evidence_builder.build(
                stable_regions.evidences,
            )
        )

        return self._diagnostic_builder.build(
            stable_regions,
            evidence,
        )
