from __future__ import annotations

from jga.domain.behaviour_evolution_model import BehaviourEvolutionModel
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


class BehaviourEvolutionBuilder:
    """
    Builds the canonical BehaviourEvolutionModel from one
    BehaviourTrajectory.

    The current implementation establishes the architectural
    contract only. Behaviour states, transitions and episodes
    will be introduced incrementally during M8.
    """

    def build(
        self,
        trajectory: BehaviourTrajectory,
    ) -> BehaviourEvolutionModel:

        return BehaviourEvolutionModel(
            trajectory=trajectory,
        )
