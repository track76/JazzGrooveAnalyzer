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


class AnalysisWindowBuilder:
    """
    JGA-155

    Builds sliding windows from PulseIntervals.
    """

    WINDOW_SIZE = 8

    STEP = 1

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        intervals = context.pulse_intervals

        if not intervals:
            context.analysis_windows = []
            return context

        windows = []

        for i in range(
            0,
            len(intervals) - self.WINDOW_SIZE + 1,
            self.STEP
        ):

            chunk = intervals[i:i + self.WINDOW_SIZE]

            windows.append(

                AnalysisWindow(

                    start_time=chunk[0].start_time,

                    end_time=chunk[-1].end_time,

                    intervals=chunk

                )

            )

        context.analysis_windows = windows

        context.log.add(
            f"{len(windows)} Analysis Windows created."
        )

        return context