"""
Measure.

Represents one measure of the Analytical Score.
"""

from dataclasses import dataclass

from jga.visualization.metric_event import (
    MetricEvent,
)


@dataclass(frozen=True, slots=True)
class Measure:
    """
    Immutable measure representation.
    """

    number: int

    time_signature: str

    bpm: float

    start_time_seconds: float = 0.0

    metric_events: tuple[MetricEvent, ...] = ()
