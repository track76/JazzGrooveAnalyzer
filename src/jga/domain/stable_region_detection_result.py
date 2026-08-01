from dataclasses import dataclass

from jga.domain.behaviour_change_event import (
    BehaviourChangeEvent,
)

from jga.domain.behaviour_comparison_evidence import (
    BehaviourComparisonEvidence,
)


@dataclass(
    frozen=True,
    slots=True,
)
class StableRegionDetectionResult:
    """
    Result of stable region detection.

    Preserves both detected events and the
    complete comparison evidence.
    """

    events: tuple[BehaviourChangeEvent, ...]

    evidences: tuple[BehaviourComparisonEvidence, ...]
