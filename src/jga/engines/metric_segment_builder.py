"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_segment_builder.py

Description:
    Builds Metric Segments from Periodicity Segments.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext


class MetricSegmentBuilder:
    """
    JGA-173

    Builds Metric Segments.
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        context.metric_segments = []

        if context.report is not None:
            context.report.metric_segments = context.metric_segments

        context.log.add(
            f"{len(context.metric_segments)} Metric Segments detected."
        )

        return context
