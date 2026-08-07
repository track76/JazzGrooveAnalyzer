"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    ensemble_analysis_engine.py

Description:
    Builds semantic ensemble analysis result.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.runtime.analysis_context import AnalysisContext


class EnsembleAnalysisEngine:
    """
    Executes ensemble semantic analysis.

    Produces:
    - SoundSource interpretation
    - MetricContributor information
    """

    def __init__(
        self,
        semantic_bridge,
        ensemble_pipeline,
    ) -> None:

        self._semantic_bridge = semantic_bridge
        self._ensemble_pipeline = ensemble_pipeline

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        sound_sources = (
            self._semantic_bridge.translate(
                context.observed_sources
            )
        )

        context.ensemble_analysis_result = (
            self._ensemble_pipeline.analyze(
                sound_sources
            )
        )

        return context
