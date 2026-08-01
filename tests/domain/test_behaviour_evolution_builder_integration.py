
from jga.domain.services.behaviour_evolution_builder import (
    BehaviourEvolutionBuilder,
)

from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.geometry.geometric_point import (
    GeometricPoint,
)

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


def create_point(value: float) -> GeometricPoint:

    return GeometricPoint(
        coordinates=(
            ScientificCoordinate(
                name="x",
                value=value,
                unit="a.u.",
            ),
        )
    )


def test_builder_populates_empty_evolution_model():

    trajectory = BehaviourTrajectory()

    model = (
        BehaviourEvolutionBuilder()
        .build(trajectory)
    )

    assert model.trajectory == trajectory
    assert model.states == ()
    assert model.transitions == ()
    assert model.episodes == ()


def test_builder_creates_evolution_structure():

    trajectory = BehaviourTrajectory(
        points=[
            create_point(0.0),
            create_point(1.0),
            create_point(2.0),
        ]
    )

    model = (
        BehaviourEvolutionBuilder()
        .build(trajectory)
    )

    assert len(model.states) == 1

    assert model.transitions == ()

    assert len(model.episodes) == 1

    assert (
        model.episodes[0]
        .stable_region_count
        == 1
    )

