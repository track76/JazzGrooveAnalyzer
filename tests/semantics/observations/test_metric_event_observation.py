from jga.semantics.observations.metric_event_observation import (
    MetricEventObservation,
)


def test_metric_event_observation():

    observation = MetricEventObservation(
        offset_ms=3.2,
        beat_index=2.0,
        absolute_time_seconds=15.73,
        source_name="Bass",
        measure_number=12,
    )

    assert observation.offset_ms == 3.2
    assert observation.beat_index == 2.0
    assert observation.source_name == "Bass"
    assert observation.measure_number == 12
