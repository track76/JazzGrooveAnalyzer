
from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.domain.behaviour_transition import (
    BehaviourTransition,
)

from jga.domain.services.evolution_episode_builder import (
    EvolutionEpisodeBuilder,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


def test_empty_input_creates_empty_episode():

    result = (
        EvolutionEpisodeBuilder()
        .build(
            (),
            (),
        )
    )

    assert result.is_empty


def test_states_and_transitions_create_episode():

    trajectory = BehaviourTrajectory()

    first = BehaviourState(
        trajectory=trajectory,
        start_index=0,
        end_index=2,
    )

    second = BehaviourState(
        trajectory=trajectory,
        start_index=5,
        end_index=8,
    )

    transition = BehaviourTransition(
        source=first,
        target=second,
    )

    result = (
        EvolutionEpisodeBuilder()
        .build(
            (
                first,
                second,
            ),
            (
                transition,
            ),
        )
    )

    assert result.stable_region_count == 2
    assert result.transition_region_count == 1

