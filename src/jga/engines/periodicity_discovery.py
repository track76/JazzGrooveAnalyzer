"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    periodicity_discovery.py

Description:
    Detects stable periodic behaviours
    inside each Source Pulse Sequence.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np

from jga.core.metric_source import MetricSource
from jga.core.periodicity_segment import PeriodicitySegment
from jga.math.regularity_scorer import RegularityScorer
from jga.runtime.analysis_context import AnalysisContext


class PeriodicityDiscovery:
    """
    JGA-231

    Searches for stable periodic behaviours.

    Version 0.4
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        segments = []

        scorer = RegularityScorer()

        if context.source_pulse_sequences:

            for sequence in context.source_pulse_sequences:

                candidates = sequence.pulse_candidates

                if len(candidates) < 2:
                    continue

                intervals = [
                    second.time - first.time
                    for first, second in zip(
                        candidates,
                        candidates[1:],
                    )
                ]

                mean_interval = (
                    sum(intervals) / len(intervals)
                )

                stability = scorer.compute(
                    np.array(intervals)
                )

                segments.append(
                    PeriodicitySegment(
                        source=sequence.source,
                        start_time=candidates[0].time,
                        end_time=candidates[-1].time,
                        mean_interval=mean_interval,
                        stability=stability,
                        confidence=1.0,
                    )
                )

        context.periodicity_segments = segments

        context.log.add(
            f"{len(segments)} Periodicity Segments discovered."
        )

        return context
