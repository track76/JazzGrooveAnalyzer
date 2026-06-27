"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    pulse_interval.py

Description:
    Represents the temporal interval between
    two consecutive Pulse Candidates.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass
class PulseInterval:
    """
    Temporal interval between two Pulse Candidates.
    """

    start_time: float

    end_time: float

    duration: float