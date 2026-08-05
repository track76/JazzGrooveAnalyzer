"""
Ensemble Microtiming Profile.

Represents collective temporal behaviour
of an ensemble at one metric position.
"""

from dataclasses import dataclass

from jga.visualization.metric_event_detail import (
    MetricEventDetail,
)


@dataclass(frozen=True, slots=True)
class EnsembleMicrotimingProfile:
    """
    Collective microtiming analysis
    for one metric position.
    """

    measure_number: int

    beat_position: float

    events: tuple[
        MetricEventDetail,
        ...

    ]

    mean_offset_ms: float

    min_offset_ms: float

    max_offset_ms: float

    spread_ms: float
