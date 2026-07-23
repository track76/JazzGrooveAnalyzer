"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_window_builder.py

Description:
    Builds sliding analysis windows.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.analysis_window import AnalysisWindow
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class AnalysisWindowBuilder:
    """
    JGA-155

    Builds sliding windows from PulseIntervals.
    """

    WINDOW_SIZE = 8

    STEP = 1

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        intervals = context.pulse_intervals

        if not intervals:

            context.analysis_windows = []

            if context.report is not None:
                context.report.analysis_windows = 0

            return context

        windows = []

        for i in range(
            0,
            len(intervals) - self.WINDOW_SIZE + 1,
            self.STEP,
        ):

            chunk = intervals[
                i:i + self.WINDOW_SIZE
            ]

            windows.append(
                AnalysisWindow(
                    start_time=chunk[0].start_time,
                    end_time=chunk[-1].end_time,
                    intervals=chunk,
                )
            )

        # Aggiorna il contesto
        context.analysis_windows = windows

        # Aggiorna il report
        if context.report is not None:
            context.report.analysis_windows = len(
                windows
            )

        context.log.add(
            RuntimeEvent(
                event_id="ANALYSIS_WINDOWS_CREATED",
                layer="ENGINE",
                component="AnalysisWindowBuilder",
                message=(
                    f"{len(windows)} "
                    "Analysis Windows created."
                ),
                input_type="list[PulseInterval]",
                output_type="list[AnalysisWindow]",
                metrics={
                    "analysis_windows": len(windows),
                },
            )
        )

        return context
