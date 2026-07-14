"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_segment.py

Description:
    Represents one observed metric behaviour
    extracted from a Periodicity Segment.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.periodicity_segment import PeriodicitySegment


@dataclass(slots=True)
class MetricSegment:
    """
    Represents one observed metric behaviour.

    A Metric Segment is produced from one
    Periodicity Segment after metric analysis.

    It does not assume any musical meter
    (4/4, 3/4, etc.).
    """

    periodicity: PeriodicitySegment

    confidence: float

    @property
    def duration(self) -> float:
        return self.periodicity.duration
