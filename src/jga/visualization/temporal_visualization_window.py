from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TemporalVisualizationWindow:
    """
    Defines the temporal interval of a scientific visualization.

    This object belongs to the Visualization Layer and expresses
    only which portion of time should be visualized.

    It performs no scientific interpretation and introduces
    no modification of the represented data.
    """

    start_time: float
    end_time: float

    def __post_init__(self) -> None:
        if self.start_time < 0:
            raise ValueError("start_time must be non-negative.")

        if self.end_time < self.start_time:
            raise ValueError(
                "end_time must be greater than or equal to start_time."
            )

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def contains(self, time: float) -> bool:
        return self.start_time <= time <= self.end_time
