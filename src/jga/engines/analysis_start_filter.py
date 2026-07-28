"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_start_filter.py

Description:
    Filters metric events before the detected
    analysis starting point.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext


class AnalysisStartFilter:
    """
    Removes Pulse Candidates occurring before
    the detected metric analysis start time.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        if (
            context.pulse_candidates is None
            or context.analysis_start_time <= 0.0
        ):
            return context

        context.pulse_candidates = [
            candidate
            for candidate in context.pulse_candidates
            if candidate.time >= context.analysis_start_time
        ]

        return context
