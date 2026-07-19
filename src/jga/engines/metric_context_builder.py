"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_context_builder.py

Description:
    Builds the observable Metric Context.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.metric_context import MetricContext
from jga.runtime.analysis_context import AnalysisContext


class MetricContextBuilder:
    """
    Builds the terminal observable Metric Context
    produced by the Observation Model.

    No musical interpretation is introduced.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        metric_context = MetricContext(
            source_pulse_sequences=tuple(
                context.source_pulse_sequences or ()
            ),
            periodicity_segments=tuple(
                context.periodicity_segments or ()
            ),
            metric_segments=tuple(
                context.metric_segments or ()
            ),
        )

        context.metric_context = metric_context

        context.log.add(
            "Metric Context created."
        )

        return context
