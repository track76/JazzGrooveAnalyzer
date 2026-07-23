"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    pulse_interval_builder.py

Description:
    Builds PulseIntervals from PulseCandidates.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.pulse_interval import PulseInterval
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class PulseBuilder:
    """
    JGA-150

    Costruisce gli intervalli temporali tra
    Pulse Candidate consecutivi.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        candidates = context.pulse_candidates

        if candidates is None or len(candidates) < 2:

            context.pulse_intervals = []

            if context.report is not None:
                context.report.pulse_intervals = 0

            return context

        intervals = []

        for previous, current in zip(
            candidates[:-1],
            candidates[1:],
        ):

            intervals.append(
                PulseInterval(
                    start_time=previous.time,
                    end_time=current.time,
                    duration=current.time
                    - previous.time,
                )
            )

        # Aggiorna il contesto
        context.pulse_intervals = intervals

        # Aggiorna il report
        if context.report is not None:
            context.report.pulse_intervals = len(intervals)

        context.log.add(
            RuntimeEvent(
                event_id="PULSE_INTERVALS_CREATED",
                layer="ENGINE",
                component="PulseBuilder",
                message=(
                    f"{len(intervals)} "
                    "Pulse Intervals created."
                ),
                input_type="list[PulseCandidate]",
                output_type="list[PulseInterval]",
                metrics={
                    "pulse_intervals": len(intervals),
                },
            )
        )

        return context
