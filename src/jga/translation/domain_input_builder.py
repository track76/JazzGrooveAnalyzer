"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py

Description:
    Default implementation of the mathematical
    transformation τ₈ (Representation Translation).

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.domain.services.ensemble_analysis_pipeline import (
    EnsembleAnalysisPipeline,
)
from jga.interfaces.translation.domain_input_builder import (
    DomainInputBuilder,
)
from jga.runtime.analysis_context import AnalysisContext
from jga.translation.tau8_translator import Tau8Translator


class DefaultDomainInputBuilder(DomainInputBuilder):
    """
    Default implementation of τ₈.

    Performs the deterministic representation
    translation from MetricContext to
    ElementaryMetricEvent domain entities.

    Before the translation, the musical domain
    is reconstructed from the AudioStem
    collection through the configured
    EnsembleAnalysisPipeline.
    """

    def __init__(
        self,
        ensemble_pipeline: EnsembleAnalysisPipeline,
    ) -> None:

        self._ensemble_pipeline = ensemble_pipeline
        self.tau8 = Tau8Translator()

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        if context is None:
            raise ValueError(
                "AnalysisContext cannot be None."
            )

        if context.audio_stems is None:
            raise ValueError(
                "AudioStemCollection required."
            )

        if context.metric_context is None:
            raise ValueError(
                "MetricContext required for τ₈ translation."
            )

        #
        # Domain reconstruction
        #

        context.ensemble_analysis_result = (
            self._ensemble_pipeline.analyze(
                tuple(context.audio_stems)
            )
        )

        #
        # Representation translation (τ₈)
        #

        context.elementary_metric_events = (
            self.tau8.translate(
                context.metric_context
            )
        )

        return context
