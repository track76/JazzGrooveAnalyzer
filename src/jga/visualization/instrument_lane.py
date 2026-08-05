"""
Instrument Lane.

Represents one instrument lane of the Analytical Score.
"""

from dataclasses import dataclass

from jga.visualization.metric_event import (
    MetricEvent,
)


@dataclass(frozen=True, slots=True)
class InstrumentLane:
    """
    Immutable instrument lane.
    """

    name: str

    metric_events: tuple[MetricEvent, ...] = ()
