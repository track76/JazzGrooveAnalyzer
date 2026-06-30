"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    periodicity_segment.py

Description:
    Represents one observed periodic segment
    of a musical source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.metric_source import MetricSource


@dataclass(slots=True)
class PeriodicitySegment:
    """
    Represents one continuous region where
    a Metric Source exhibits a stable
    periodic behaviour.

    This class does NOT state that the
    source is metric.

    It only describes an observed
    periodic behaviour.
    """

    # Source

    source: MetricSource

    # Time interval

    start_time: float

    end_time: float

    # Average interval between events

    mean_interval: float

    # Regularity score

    stability: float

    # Reliability of the observation

    confidence: float

    @property
    def duration(self) -> float:

        return self.end_time - self.start_time