from tests.support.domain_objects import (
    make_internal_metric_timeline,
)

from jga.domain.services.behaviour_observation_builder import (
    BehaviourObservationBuilder,
)


def test_behaviour_observation_builder_creates_one_observation_per_pulse():

    timeline = make_internal_metric_timeline()

    builder = BehaviourObservationBuilder()

    observations = builder.build(
        timeline,
    )

    assert len(observations) == len(
        timeline.pulses
    )
