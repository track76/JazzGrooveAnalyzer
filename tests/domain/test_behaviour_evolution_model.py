from jga.domain.behaviour_evolution_model import BehaviourEvolutionModel
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def test_empty_evolution_model():

    trajectory = BehaviourTrajectory()

    model = BehaviourEvolutionModel(
        trajectory=trajectory,
    )

    assert model.trajectory is trajectory
    assert model.state_count == 0
    assert model.transition_count == 0
    assert model.episode_count == 0
