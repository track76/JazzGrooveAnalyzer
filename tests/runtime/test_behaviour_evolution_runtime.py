
from jga.geometry.behaviour_trajectory import (
    BehaviourTrajectory,
)

from jga.geometry.scientific_behaviour_space import (
    ScientificBehaviourSpace,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.runtime.engines.behaviour_observation_runner import (
    BehaviourObservationRunner,
)


def test_behaviour_evolution_is_generated_in_runtime():

    context = AnalysisContext(audio=None)

    context.scientific_behaviour_space = (
        ScientificBehaviourSpace(
            trajectories=[
                BehaviourTrajectory()
            ]
        )
    )

    BehaviourObservationRunner().run(
        context
    )

    assert (
        context.behaviour_evolution_model
        is not None
    )

    assert (
        context.behaviour_evolution_model
        .trajectory
        ==
        context.scientific_behaviour_space
        .first_trajectory
    )

