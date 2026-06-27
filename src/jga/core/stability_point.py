"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stability_point.py

Description:
    Represents one point of the Metric Stability Curve.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class StabilityPoint:
    """
    One point of the Metric Stability Curve.
    """

    # Tempo (secondi)
    time: float

    # Stability Score [0..1]
    score: float

    # Numero di PulseInterval utilizzati
    window_size: int