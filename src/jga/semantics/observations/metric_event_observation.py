"""
Metric Event Observation.

Observable information used by the Semantic Layer.

This object contains only observable facts.
It contains no semantic interpretation.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricEventObservation:
    """
    Observable properties associated with one
    Metric Event.
    """

    offset_ms: float

    beat_index: float

    absolute_time_seconds: float

    source_name: str

    measure_number: int
