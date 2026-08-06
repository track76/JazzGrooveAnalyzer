from jga.semantics.observations.metric_event_observation import (
    MetricEventObservation,
)
from jga.semantics.services.timing_behaviour_service import (
    TimingBehaviourService,
)
from jga.semantics.timing_behaviour import (
    TimingBehaviour,
)


def test_unknown_without_threshold():

    observation = MetricEventObservation(
        offset_ms=0.0,
        beat_index=1.0,
        absolute_time_seconds=0.0,
        source_name="Bass",
        measure_number=1,
    )

    service = TimingBehaviourService()

    assert (
        service.classify(observation)
        is TimingBehaviour.UNKNOWN
    )
