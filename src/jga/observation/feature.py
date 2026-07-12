"""
=========================================================
Jazz Groove Analyzer (JGA)

Feature Observation Object

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    """
    Observable feature extracted from an onset.

    This object belongs to the Observation Domain.
    """

    time: float
