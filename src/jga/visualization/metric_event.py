"""
Metric Event.

Represents one significant metric event in the
Analytical Score.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricEvent:
    """
    Immutable metric event.
    """

    beat_index: int

    offset_ms: float
