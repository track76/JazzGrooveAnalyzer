
from __future__ import annotations

from jga.domain.behaviour_evolution_model import (
    BehaviourEvolutionModel,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.domain.services.behaviour_state_segmenter import (
    BehaviourStateSegmenter,
)

from jga.domain.services.default_behaviour_state_segmenter import (
    DefaultBehaviourStateSegmenter,
)

from jga.domain.services.behaviour_transition_builder import (
    BehaviourTransitionBuilder,
)

from jga.domain.services.evolution_episode_builder import (
    EvolutionEpisodeBuilder,
)


class BehaviourEvolutionBuilder:
    """
    Builds the canonical BehaviourEvolutionModel
    from one BehaviourTrajectory.

    The builder orchestrates the complete evolution
    reconstruction chain.
    """

    def __init__(
        self,
        state_segmenter: BehaviourStateSegmenter | None = None,
        transition_builder: BehaviourTransitionBuilder | None = None,
        episode_builder: EvolutionEpisodeBuilder | None = None,
    ) -> None:

        self._state_segmenter = (
            state_segmenter
            or DefaultBehaviourStateSegmenter()
        )

        self._transition_builder = (
            transition_builder
            or BehaviourTransitionBuilder()
        )

        self._episode_builder = (
            episode_builder
            or EvolutionEpisodeBuilder()
        )

    def build(
        self,
        trajectory: BehaviourTrajectory,
    ) -> BehaviourEvolutionModel:

        states = (
            self._state_segmenter
            .segment(trajectory)
        )

        transitions = (
            self._transition_builder
            .build(states)
        )

        episode = (
            self._episode_builder
            .build(
                states,
                transitions,
            )
        )

        return BehaviourEvolutionModel(
            trajectory=trajectory,
            states=states,
            transitions=transitions,
            episodes=(
                (episode,)
                if states
                else ()
            ),
        )

