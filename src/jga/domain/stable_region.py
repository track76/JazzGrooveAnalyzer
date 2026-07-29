from __future__ import annotations

from dataclasses import dataclass

from jga.domain.behaviour_state import BehaviourState


@dataclass(frozen=True)
class StableRegion:
    """
    Represents a temporally stable behavioural region.

    A StableRegion is the temporal manifestation of exactly
    one BehaviourState.
    """

    state: BehaviourState

    @property
    def start_index(self) -> int:
        return self.state.start_index

    @property
    def end_index(self) -> int:
        return self.state.end_index

    @property
    def duration(self) -> int:
        return self.state.duration
