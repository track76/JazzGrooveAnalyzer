"""
Measure Timeline.

Visualization representation of metric events
inside one reconstructed measure.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MeasureTimeline:
    """
    Immutable visualization timeline
    for one measure.
    """

    measure_number: int

    beats: tuple[int, ...]

    offsets_ms: tuple[float, ...]
