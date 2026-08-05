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

    source_name: str = ""

    beat_index: int = 0

    absolute_time_seconds: float = 0.0

    offset_ms: float = 0.0
