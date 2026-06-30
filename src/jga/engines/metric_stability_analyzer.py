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

from jga.math.stability_scorer import StabilityScorer

from jga.runtime.analysis_context import AnalysisContext


class MetricStabilityAnalyzer:
    """
    JGA-160

    Computes the Metric Stability Curve.
    """

    def __init__(self):

        self.scorer = StabilityScorer()

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        windows = context.analysis_windows

        curve = StabilityCurve()

        if not windows:

            context.stability_curve = curve

            if context.report is not None:
                context.report.stability_curve = curve

            return context

        for window in windows:

            durations = np.array(
                [interval.duration for interval in window.intervals]
            )

            score = self.scorer.compute(durations)

            point = StabilityPoint(
                time=(window.start_time + window.end_time) / 2,
                score=score,
                window_size=window.size
            )

            curve.add(point)

        # Aggiorna il contesto
        context.stability_curve = curve

        # Aggiorna il report
        if context.report is not None:
            context.report.stability_curve = curve

        context.log.add(
            f"{len(curve)} Stability Points computed."
        )

        return context