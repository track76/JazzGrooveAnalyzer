from jga.domain.observable_metric_context import (
    ObservableMetricContext,
)


def test_observable_metric_context_creation():

    context = ObservableMetricContext(
        observed_meter="4/4",
        local_tempo=120.0,
        confidence=0.95,
    )

    assert context.observed_meter == "4/4"
    assert context.local_tempo == 120.0
    assert context.confidence == 0.95
