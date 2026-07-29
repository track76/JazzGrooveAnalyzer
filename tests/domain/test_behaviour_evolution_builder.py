from jga.domain.behaviour_evolution_model import BehaviourEvolutionModel
from jga.domain.services.behaviour_evolution_builder import (
    BehaviourEvolutionBuilder,
)
from jga.geometry.behaviour_trajectory import BehaviourTrajectory


def test_builder_returns_empty_evolution_model():

    trajectory = BehaviourTrajectory()

    builder = BehaviourEvolutionBuilder()

    model = builder.build(trajectory)

    assert isinstance(model, BehaviourEvolutionModel)
    assert model.trajectory is trajectory
    assert model.state_count == 0
    assert model.transition_count == 0
    assert model.episode_count == 0
