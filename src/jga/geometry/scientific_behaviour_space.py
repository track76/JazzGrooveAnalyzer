from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from jga.geometry.behaviour_trajectory import BehaviourTrajectory


@dataclass(frozen=True)
class ScientificBehaviourSpace:
    """
    Scientific representation of the complete behaviour space.

    This object belongs to the Geometry layer.
    """

    trajectories: list[BehaviourTrajectory] = field(default_factory=list)

    @property
    def trajectory_count(self) -> int:
        return len(self.trajectories)

    @property
    def is_empty(self) -> bool:
        return len(self.trajectories) == 0

    @property
    def first_trajectory(self) -> BehaviourTrajectory | None:
        return None if self.is_empty else self.trajectories[0]

    def __iter__(self) -> Iterator[BehaviourTrajectory]:
        return iter(self.trajectories)

