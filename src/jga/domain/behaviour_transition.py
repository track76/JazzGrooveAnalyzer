from __future__ import annotations

from dataclasses import dataclass

from jga.domain.behaviour_state import BehaviourState


@dataclass(frozen=True)
class BehaviourTransition:
    """
    Represents one observable transition between two
    consecutive BehaviourStates.
    """

    source: BehaviourState
    target: BehaviourState

    def __post_init__(self) -> None:

        if self.source.end_index >= self.target.start_index:
            raise ValueError(
                "Transition requires two non-overlapping consecutive states."
            )

    @property
    def duration(self) -> int:
        return self.target.start_index - self.source.end_index - 1
