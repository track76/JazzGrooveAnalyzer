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

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self):
        return iter(self.events)

    def __getitem__(self, index):
        return self.events[index]

    def __eq__(self, other) -> bool:

        if other == ():
            return self.events == ()

        return super().__eq__(other)
