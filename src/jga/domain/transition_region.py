from __future__ import annotations

from dataclasses import dataclass

from jga.domain.behaviour_transition import BehaviourTransition


@dataclass(frozen=True)
class TransitionRegion:
    """
    Represents a temporally observable behavioural transition.

    A TransitionRegion is the temporal manifestation of exactly
    one BehaviourTransition.
    """

    transition: BehaviourTransition

    @property
    def start_index(self) -> int:
        return self.transition.source.end_index + 1

    @property
    def end_index(self) -> int:
        return self.transition.target.start_index - 1

    @property
    def duration(self) -> int:
        return self.transition.duration
