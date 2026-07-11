"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    rhythmic_behaviour.py

Description:
    Observed rhythmic behaviour of one AudioStem.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass
class RhythmicBehaviour:
    """
    Rhythmic behaviour observed for one AudioStem.
    """

    source_name: str

    periodicity: float

    persistence: float

    continuity: float

    metric_compatibility: float

    confidence: float = 1.0