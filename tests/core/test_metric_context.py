from pytest import raises

from jga.core.metric_context import MetricContext
from jga.core.metric_segment import MetricSegment
from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment


def make_metric_segment() -> MetricSegment:
    periodicity = PeriodicitySegment(
        source=MetricSource(
            name="Ride",
            family="Percussion",
        ),
        start_time=0.0,
        end_time=2.0,
        mean_interval=0.5,
        stability=0.95,
        confidence=0.90,
    )

    return MetricSegment(
        periodicity=periodicity,
        confidence=0.90,
    )


def test_metric_context_requires_segments():
    with raises(ValueError):
        MetricContext(metric_segments=())


def test_metric_context_exposes_segment_count():
    context = MetricContext(
        metric_segments=(
            make_metric_segment(),
            make_metric_segment(),
        )
    )

    assert context.segment_count == 2
