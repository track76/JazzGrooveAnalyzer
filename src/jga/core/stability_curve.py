"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stability_curve.py

Description:
    Metric Stability Curve.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

from jga.core.stability_point import StabilityPoint


@dataclass
class StabilityCurve:
    """
    Collection of StabilityPoint objects.
    """

    points: list[StabilityPoint] = field(default_factory=list)

    def add(self, point: StabilityPoint) -> None:
        self.points.append(point)

    def __len__(self) -> int:
        return len(self.points)

    def __iter__(self):
        return iter(self.points)