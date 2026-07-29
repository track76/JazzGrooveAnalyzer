from jga.domain.behaviour_state import BehaviourState
from jga.domain.behaviour_transition import BehaviourTransition
from jga.domain.stable_region import StableRegion
from jga.domain.transition_region import TransitionRegion
from jga.domain.evolution_episode import EvolutionEpisode
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def trajectory():
    return BehaviourTrajectory()


def test_empty_episode():

    episode = EvolutionEpisode()

    assert episode.is_empty
    assert episode.stable_region_count == 0
    assert episode.transition_region_count == 0


def test_episode_counts():

    t = trajectory()

    s1 = BehaviourState(t, 0, 4)
    s2 = BehaviourState(t, 7, 10)

    stable = StableRegion(s1)

    transition = TransitionRegion(
        BehaviourTransition(s1, s2)
    )

    episode = EvolutionEpisode(
        stable_regions=(stable,),
        transition_regions=(transition,),
    )

    assert not episode.is_empty
    assert episode.stable_region_count == 1
    assert episode.transition_region_count == 1
