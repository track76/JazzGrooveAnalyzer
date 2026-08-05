"""
Analytical Groove Point.

Visualization-level representation of a metric event.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AnalyticalGroovePoint:
    """
    Single point for analytical groove visualization.
    """

    measure_number: int
    instrument: str

    theoretical_beat: float

    absolute_time_seconds: float

    bpm: float

    offset_ms: float

    @property
    def beat_duration_seconds(self) -> float:
        return 60.0 / self.bpm

    @property
    def normalized_position(self) -> float:
        """
        Real metric position including temporal deviation.
        """

        return self.theoretical_beat
