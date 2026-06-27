"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_stability_analyzer.py

Description:
    Computes the Metric Stability Curve.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np

from jga.core.stability_curve import StabilityCurve
from jga.core.stability_point import StabilityPoint
from jga.runtime.analysis_context import AnalysisContext


class MetricStabilityAnalyzer:
    """
    JGA-160

    Computes the Metric Stability Curve.
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        windows = context.analysis_windows

        curve = StabilityCurve()

        if not windows:
            context.stability_curve = curve
            return context

        for window in windows:

            durations = np.array(
                [i.duration for i in window.intervals]
            )

            mean = np.mean(durations)

            std = np.std(durations)

            if mean == 0:
                score = 0.0
            else:
                cv = std / mean
                score = 1.0 / (1.0 + cv)

            point = StabilityPoint(

                time=(window.start_time + window.end_time) / 2,

                score=float(score),

                window_size=window.size

            )

            curve.add(point)

        context.stability_curve = curve

        context.log.add(
            f"{len(curve)} Stability Points computed."
        )

        return context