"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    eme.py

Description:
    Elementary Metric Event (EME)

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.metric_position import MetricPosition


@dataclass
class EME:
    """
    Elementary Metric Event.

    Represents a single rhythmic event detected from one
    rhythmic source and assigned to a specific metric position.

    The EME is the elementary temporal unit of the
    Jazz Groove Analyzer (JGA).

    NOTE
    ----
    An EME does NOT belong to a Metric Cluster yet.
    Cluster assignment is performed by the Cluster Engine.
    """

    # Progressive identifier
    id: int

    # Rhythmic source identifier
    source_id: str

    # Instrument name
    instrument: str

    # Metric position inside the piece
    metric_position: MetricPosition

    # Physical onset (seconds)
    physical_onset: float

    # Perceived onset (seconds)
    perceived_onset: float

    # Detection confidence (0.0 - 1.0)
    confidence: float

    @property
    def timing_difference(self) -> float:
        """
        Difference between perceived and physical onset.
        """

        return self.perceived_onset - self.physical_onset

    def __str__(self) -> str:

        return (
            f"EME #{self.id} | "
            f"{self.instrument} | "
            f"{self.metric_position}"
        )