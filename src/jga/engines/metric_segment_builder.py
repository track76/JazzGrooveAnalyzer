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

from jga.core.metric_segment import MetricSegment
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class MetricSegmentBuilder:
    """
    JGA-173

    Builds Metric Segments.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        metric_segments = []

        periodicity_segments = (
            context.periodicity_segments or []
        )

        for segment in periodicity_segments:

            metric_segments.append(
                MetricSegment(
                    periodicity=segment,
                    confidence=segment.confidence,
                )
            )

        context.metric_segments = metric_segments

        if context.report is not None:
            context.report.metric_segments = (
                metric_segments
            )

        context.log.add(
            RuntimeEvent(
                event_id="METRIC_SEGMENTS_CREATED",
                layer="ENGINE",
                component="MetricSegmentBuilder",
                message=(
                    f"{len(metric_segments)} "
                    "Metric Segments detected."
                ),
                input_type="list[PeriodicitySegment]",
                output_type="list[MetricSegment]",
                metrics={
                    "metric_segments": len(
                        metric_segments
                    ),
                },
            )
        )

        return context
