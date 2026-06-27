"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_position.py

Description:
    Defines the musical position of an event within
    the metric structure of the ensemble.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MetricPosition:
    """
    Represents the metric position of a musical event.

    This object does not contain timing information.
    It only identifies where the event belongs inside
    the metric structure.

    Example:
        Segment      = 0
        Measure      = 125
        Beat         = 3
        Subdivision  = "beat"
    """

    # Metric segment identifier
    segment_id: int

    # Measure number
    measure: int

    # Beat number inside the measure
    beat: int

    # Optional metric subdivision
    subdivision: Optional[str] = None

    def __str__(self) -> str:

        if self.subdivision:
            return (
                f"Segment {self.segment_id} | "
                f"Measure {self.measure} | "
                f"Beat {self.beat} | "
                f"{self.subdivision}"
            )

        return (
            f"Segment {self.segment_id} | "
            f"Measure {self.measure} | "
            f"Beat {self.beat}"
        )