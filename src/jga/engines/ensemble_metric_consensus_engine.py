"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    ensemble_metric_consensus_engine.py

Description:
    Pipeline adapter for Ensemble Metric Consensus.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.engines.ensemble_metric_consensus import (
    EnsembleMetricConsensus,
)

from jga.runtime.analysis_context import AnalysisContext


class EnsembleMetricConsensusEngine:
    """
    Pipeline boundary for Ensemble Metric Consensus.
    """

    def __init__(self):

        self.consensus = (
            EnsembleMetricConsensus()
        )

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        pulse_candidates = (
            context.domain_pulse_candidates
        )

        context.ensemble_metric_events = (
            self.consensus.build(
                pulse_candidates,
                context.metric_contributors,
            )
        )

        context.log.add(
            f"{len(context.ensemble_metric_events)} "
            "Ensemble Metric Events created."
        )

        return context
