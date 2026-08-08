"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stable_region_detector.py

Description:
    Detects Persistent Stable Regions from a Stability Curve.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint
from jga.core.stable_region import StableRegion


class StableRegionDetector:

    STABILITY_THRESHOLD = 0.75
    MIN_POINTS = 3

    def detect(
        self,
        stability_curve: StabilityCurve,
    ) -> list[StableRegion]:

        regions: list[StableRegion] = []
        current: list[StabilityPoint] = []

        for point in stability_curve:

            if point.score >= self.STABILITY_THRESHOLD:
                current.append(point)
                continue

            if len(current) >= self.MIN_POINTS:
                regions.append(
                    StableRegion(
                        start_time=current[0].time,
                        end_time=current[-1].time,
                        stability_points=tuple(current),
                    )
                )

            current = []

        if len(current) >= self.MIN_POINTS:
            regions.append(
                StableRegion(
                    start_time=current[0].time,
                    end_time=current[-1].time,
                    stability_points=tuple(current),
                )
            )

        return regions
