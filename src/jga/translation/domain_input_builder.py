"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py

Description:
    Canonical Domain reconstruction pipeline.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.domain.services.behaviour_construction_builder import (
    BehaviourConstructionBuilder,
)
from jga.domain.services.ensemble_analysis_pipeline import (
    EnsembleAnalysisPipeline,
)
from jga.interfaces.translation.domain_input_builder import (
    DomainInputBuilder,
)
from jga.runtime.analysis_context import AnalysisContext
from jga.translation.semantic_bridge import (
    SemanticBridge,
)
from jga.translation.domain_reconstruction_input_builder import (
    DomainReconstructionInputBuilder,
)
from jga.translation.domain_reconstruction_builder import (
    DefaultDomainReconstructionBuilder,
)
from jga.translation.tau8_translator import Tau8Translator


from jga.semantics.builders.metric_event_semantics_builder import (
    MetricEventSemanticsBuilder,
)

class DefaultDomainInputBuilder(DomainInputBuilder):
    """
    Canonical Domain reconstruction pipeline.

        τ₈
         ↓
    ElementaryMetricEvent
         ↓
      BeatReference
         ↓
      MetricCluster
         ↓
          Pulse
         ↓
 InternalMetricTimeline
         ↓
 BehaviourObservation
         ↓
   BehaviourProfile
    """

    def __init__(
        self,
        semantic_bridge: SemanticBridge,
        ensemble_pipeline: EnsembleAnalysisPipeline,
    ) -> None:

        self._semantic_bridge = semantic_bridge

        self._ensemble_pipeline = ensemble_pipeline

        self.reconstruction_input_builder = (
            DomainReconstructionInputBuilder()
        )

        self.domain_reconstruction_builder = (
            DefaultDomainReconstructionBuilder()
        )

        self.tau8 = Tau8Translator()

        self.behaviour_construction_builder = (
            BehaviourConstructionBuilder()
        )

    def build(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        if context is None:
            raise ValueError(
                "AnalysisContext cannot be None."
            )

        if context.observed_sources is None:
            raise ValueError(
                "ObservedSourceCollection required."
            )

        if context.metric_context is None:
            raise ValueError(
                "MetricContext required."
            )

        #
        # Ensemble understanding
        #

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

        #
        # τ₈
        #

        context.domain_pulse_candidates = (
            self.tau8.translate(
                context.metric_context,
                sound_sources,
            )
        )

        reconstruction_input = (
            self.reconstruction_input_builder.build(
                context
            )
        )

        context.metric_contributors = (
            reconstruction_input.metric_contributors
        )

        #
        # Elementary Metric Events
        #

        reconstruction_result = (
            self.domain_reconstruction_builder.build(
                reconstruction_input
            )
        )

        context.elementary_metric_events = (
            reconstruction_result.elementary_metric_events
        )

        builder = MetricEventSemanticsBuilder()

        context.semantics = tuple(
            builder.build()
            for _ in context.elementary_metric_events
        )

        context.beat_references = (
            reconstruction_result.beat_references
        )

        context.metric_clusters = (
            reconstruction_result.metric_clusters
        )

        context.pulses = (
            reconstruction_result.pulses
        )

        context.internal_metric_timeline = (
            reconstruction_result.internal_metric_timeline
        )

        if context.internal_metric_timeline is None:
            return context

        #
        # Behaviour Observations
        #

        behaviour_result = (
            self.behaviour_construction_builder.build(
                context.internal_metric_timeline,
            )
        )

        context.behaviour_observations = (
            behaviour_result.behaviour_observations
        )

        context.behaviour_profile = (
            behaviour_result.behaviour_profile
        )

        return context