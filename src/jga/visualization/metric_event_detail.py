"""
Metric Event Detail.

Scientific detail representation of one
metric event for inspection.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MetricEventDetail:
    """
    Detailed analytical representation
    of one metric event.
    """

    source_name: str

    measure_number: int

    theoretical_position: float

    observed_position: float

    beat_position: float

    offset_ms: float

    bpm: float

    @property
    def beat_duration_ms(self) -> float:
        return (
            60000.0 / self.bpm
        )

    @property
    def deviation_ratio(self) -> float:
        """
        Temporal deviation normalized
        on beat duration.
        """

        if self.beat_duration_ms == 0:
            return 0.0

        return (
            self.offset_ms
            /
            self.beat_duration_ms
        )
