"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py

Description:
    Default implementation of the
    Domain Input construction boundary.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.domain.services.elementary_metric_event_builder import (
    ElementaryMetricEventBuilder,
)
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
    Builds the canonical Domain input.

    Responsibilities:

    1. Reconstruct the musical domain.
    2. Apply τ₈ representation translation.
    3. Build ElementaryMetricEvent entities.
    """

    def __init__(
        self,
        ensemble_pipeline: EnsembleAnalysisPipeline,
    ) -> None:

        self._ensemble_pipeline = ensemble_pipeline

        self.tau8 = Tau8Translator()

        self.eme_builder = (
            ElementaryMetricEventBuilder()
        )

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
        # τ₈ Representation Translation
        #

        context.domain_pulse_candidates = (
            self.tau8.translate(
                context.metric_context,
                context.ensemble_analysis_result.sound_sources,
            )
        )

        #
        # Domain Metric Event construction
        #

        context.elementary_metric_events = (
            self.eme_builder.build(
                context.domain_pulse_candidates,
                context.ensemble_analysis_result.metric_contributors,
            )
        )

        return context
