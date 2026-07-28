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
from jga.runtime.runtime_event import RuntimeEvent


class AnalysisStartFilter:
    """
    Removes Pulse Candidates occurring before
    the detected metric analysis start time.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        if context.pulse_candidates is None:
            return context

        if context.analysis_start_time <= 0.0:
            return context

        context.pulse_candidates = [
            candidate
            for candidate in context.pulse_candidates
            if candidate.time >= context.analysis_start_time
        ]

        context.log.add(
            RuntimeEvent(
                event_id="ANALYSIS_START_FILTER_APPLIED",
                layer="ENGINE",
                component="AnalysisStartFilter",
                message=(
                    f"{len(context.pulse_candidates)} "
                    "Pulse Candidates after analysis start filtering."
                ),
                input_type="list[PulseCandidate]",
                output_type="list[PulseCandidate]",
                metrics={
                    "analysis_start_time": (
                        context.analysis_start_time
                    ),
                    "pulse_candidates": (
                        len(context.pulse_candidates)
                    ),
                },
            )
        )

        return context
