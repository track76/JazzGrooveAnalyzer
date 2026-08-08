"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stable_region.py

Description:
    Represents a Persistent Stable Region.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.stability_point import StabilityPoint


@dataclass(frozen=True)
class StableRegion:
    """
    Represents a contiguous metrically stable region.
    """

    start_time: float
    end_time: float
    stability_points: tuple[StabilityPoint, ...]

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    @property
    def size(self) -> int:
        return len(self.stability_points)

    @property
    def mean_score(self) -> float:
        if not self.stability_points:
            return 0.0

        return sum(
            point.score
            for point in self.stability_points
        ) / len(self.stability_points)
