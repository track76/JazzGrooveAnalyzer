from __future__ import annotations

from dataclasses import dataclass

from jga.geometry.behaviour_trajectory import BehaviourTrajectory


@dataclass(frozen=True)
class BehaviourState:
    """
    Represents one locally coherent behavioural state
    observed inside one BehaviourTrajectory.
    """

    trajectory: BehaviourTrajectory

    start_index: int

    end_index: int

    def __post_init__(self) -> None:

        if self.start_index < 0:
            raise ValueError("start_index must be non-negative")

        if self.end_index < self.start_index:
            raise ValueError(
                "end_index must be greater than or equal to start_index"
            )

    @property
    def duration(self) -> int:
        return self.end_index - self.start_index + 1
