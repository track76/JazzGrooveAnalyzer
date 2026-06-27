"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_window.py

Description:
    Sliding analysis window.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

from jga.core.pulse_interval import PulseInterval


@dataclass(slots=True)
class AnalysisWindow:
    """
    One sliding analysis window.
    """

    start_time: float

    end_time: float

    intervals: list[PulseInterval] = field(default_factory=list)

    @property
    def size(self) -> int:
        return len(self.intervals)