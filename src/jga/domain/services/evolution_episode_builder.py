
from __future__ import annotations

from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.domain.behaviour_transition import (
    BehaviourTransition,
)

from jga.domain.evolution_episode import (
    EvolutionEpisode,
)

from jga.domain.stable_region import (
    StableRegion,
)

from jga.domain.transition_region import (
    TransitionRegion,
)


class EvolutionEpisodeBuilder:
    """
    Builds an EvolutionEpisode from validated
    BehaviourStates and BehaviourTransitions.

    No analytical decision is performed here.
    The builder only translates existing domain
    objects into temporal regions.
    """

    def build(
        self,
        states: tuple[BehaviourState, ...],
        transitions: tuple[BehaviourTransition, ...],
    ) -> EvolutionEpisode:

        stable_regions = tuple(
            StableRegion(
                state=state,
            )
            for state in states
        )

        transition_regions = tuple(
            TransitionRegion(
                transition=transition,
            )
            for transition in transitions
        )

        return EvolutionEpisode(
            stable_regions=stable_regions,
            transition_regions=transition_regions,
        )

