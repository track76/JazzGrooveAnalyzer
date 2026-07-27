from jga.geometry.behaviour_trajectory import BehaviourTrajectory
from jga.geometry.scientific_behaviour_space import ScientificBehaviourSpace


def test_empty():

    space = ScientificBehaviourSpace()

    assert space.is_empty
    assert space.trajectory_count == 0
    assert space.first_trajectory is None


def test_iteration():

    trajectory = BehaviourTrajectory()

    space = ScientificBehaviourSpace(
        trajectories=[trajectory],
    )

    assert list(space) == [trajectory]

