"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_segment.py

Description:
    Metric Segment

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass
class MetricSegment:
    """
    Represents a portion of the musical performance
    in which the meter remains constant.
    """

    id: int

    start_measure: int

    end_measure: int

    numerator: int

    denominator: int

    detection_mode: str = "automatic"

    confidence: float = 1.0

    @property
    def meter(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __str__(self) -> str:
        return (
            f"Segment {self.id} | "
            f"Measures {self.start_measure}-{self.end_measure} | "
            f"{self.meter}"
        )