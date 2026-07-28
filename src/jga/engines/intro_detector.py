"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    intro_detector.py

Description:
    Intro Detection Engine

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.stability_curve import (
    StabilityCurve,
)


@dataclass
class IntroDetectionResult:
    """
    Result of the intro detection process.
    """

    analysis_start_time: float

    confidence: float


class IntroDetector:
    """
    Intro Detection Engine.

    Detects the first metrically stable region
    from the Metric Stability Curve.
    """

    STABILITY_THRESHOLD = 0.75

    def detect(
        self,
        stability_curve: StabilityCurve,
    ) -> IntroDetectionResult:

        for point in stability_curve:

            if (
                point.score
                >= self.STABILITY_THRESHOLD
            ):
                return IntroDetectionResult(
                    analysis_start_time=point.time,
                    confidence=point.score,
                )

        return IntroDetectionResult(
            analysis_start_time=0.0,
            confidence=0.0,
        )
