from __future__ import annotations

from dataclasses import dataclass, field

from jga.geometry.behaviour_trajectory import BehaviourTrajectory


@dataclass(frozen=True)
class BehaviourEvolutionModel:
    """
    Root aggregate of Behaviour Evolution.

    Represents the complete observable temporal evolution of one
    BehaviourTrajectory.
    """

    trajectory: BehaviourTrajectory

    states: tuple = field(default_factory=tuple)

    transitions: tuple = field(default_factory=tuple)

    episodes: tuple = field(default_factory=tuple)

    @property
    def state_count(self) -> int:
        return len(self.states)

    @property
    def transition_count(self) -> int:
        return len(self.transitions)

    @property
    def episode_count(self) -> int:
        return len(self.episodes)
