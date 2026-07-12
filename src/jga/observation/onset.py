"""
=========================================================
Jazz Groove Analyzer (JGA)

Onset Observation Object

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Onset:
    """
    Observable onset event.

    An onset represents the perceptual beginning of a sound event.

    It belongs to the Observation Domain.
    """

    time: float
