
from jga.domain.behaviour_state import (
    BehaviourState,
)

from jga.domain.services.behaviour_evolution_builder import (
    BehaviourEvolutionBuilder,
)

from jga.domain.services.behaviour_state_segmenter import (
    BehaviourStateSegmenter,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)


class DummyBehaviourStateSegmenter(
    BehaviourStateSegmenter
):
    """
    Controlled segmenter used only for
    evolution chain validation.
    """

    def segment(
        self,
        trajectory,
    ):

        return (
            BehaviourState(
                trajectory=trajectory,
                start_index=0,
                end_index=1,
            ),

            BehaviourState(
                trajectory=trajectory,
                start_index=3,
                end_index=4,
            ),
        )


def test_full_behaviour_evolution_chain():

    trajectory = BehaviourTrajectory()

    model = (
        BehaviourEvolutionBuilder(
            state_segmenter=(
                DummyBehaviourStateSegmenter()
            )
        )
        .build(trajectory)
    )

    assert len(model.states) == 2

    assert len(model.transitions) == 1

    assert len(model.episodes) == 1

    episode = model.episodes[0]

    assert (
        episode.stable_region_count
        == 2
    )

    assert (
        episode.transition_region_count
        == 1
    )

