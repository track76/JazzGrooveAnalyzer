"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_pipeline.py

Description:
    Main analysis pipeline.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.audio.file_audio_source import FileAudioSource

from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.intro_detector import IntroDetector

from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.engines.pulse_builder import PulseBuilder
from jga.engines.analysis_window_builder import AnalysisWindowBuilder
from jga.engines.metric_stability_analyzer import MetricStabilityAnalyzer
from jga.engines.source_pulse_extractor import SourcePulseExtractor
from jga.engines.periodicity_discovery import PeriodicityDiscovery
from jga.engines.metric_segment_builder import MetricSegmentBuilder
from jga.engines.metric_context_builder import MetricContextBuilder
from jga.engines.metric_cluster_builder import MetricClusterBuilder

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.analysis_report import AnalysisReport

from jga.separation.null_separator import NullSeparator

from jga.domain.services.dummy_source_identification_service import (
    DummySourceIdentificationService,
)
from jga.domain.services.rule_based_ensemble_analysis_pipeline import (
    RuleBasedEnsembleAnalysisPipeline,
)
from jga.domain.services.rule_based_metric_contributor_assignment_service import (
    RuleBasedMetricContributorAssignmentService,
)
from jga.domain.services.rule_based_musical_function_assignment_service import (
    RuleBasedMusicalFunctionAssignmentService,
)

from jga.translation.domain_input_builder import (
    DefaultDomainInputBuilder,
)

from jga.domain.services.rule_based_behaviour_analytics_pipeline import (
    RuleBasedBehaviourAnalyticsPipeline,
)


class AnalysisPipeline:
    """
    Main JGA analysis pipeline.
    """

    def __init__(self):

        self.loader = FileAudioSource()

        self.preprocessor = AudioPreprocessor()

        self.separator = NullSeparator()

        self.intro_detector = IntroDetector()

        self.pulse_detector = PulseCandidateBuilder()

        self.pulse_filter = PulseCandidateFilter()

        self.interval_builder = PulseBuilder()

        self.window_builder = AnalysisWindowBuilder()

        self.stability = MetricStabilityAnalyzer()

        self.source_pulse_extractor = SourcePulseExtractor()

        self.periodicity_discovery = PeriodicityDiscovery()

        self.metric_segment_builder = MetricSegmentBuilder()

        self.metric_context_builder = MetricContextBuilder()

        self.metric_cluster_builder = MetricClusterBuilder()
        
        source_identifier = DummySourceIdentificationService()

        function_assigner = (
            RuleBasedMusicalFunctionAssignmentService()
        )

        contributor_assigner = (
            RuleBasedMetricContributorAssignmentService()
        )
 
        ensemble_pipeline = (
            RuleBasedEnsembleAnalysisPipeline(
                source_identifier=source_identifier,
                function_assigner=function_assigner,
                contributor_assigner=contributor_assigner,
            )
        )

        self.domain_input_builder = (
            DefaultDomainInputBuilder(
                ensemble_pipeline=ensemble_pipeline,
            )
        )

        self.behaviour_analytics_pipeline = (
            RuleBasedBehaviourAnalyticsPipeline()
        )
 
    def analyze(
        self,
        filepath: str
    ) -> AnalysisContext:

        # Audio loading
        audio = self.loader.load(filepath)

        context = AnalysisContext(audio=audio)

        context.report = AnalysisReport(audio=audio)

        context.log.add("Audio loaded.")

        # Preprocessing
        context = self.preprocessor.process(context)

        # Source separation
        context = self.separator.process(context)

        # Intro detection
        intro = self.intro_detector.detect(context.audio)

        context.log.add(
            f"Analysis starts at {intro.analysis_start_time:.3f} s"
        )

        # Pulse Candidates
        context = self.pulse_detector.process(context)

        context = self.pulse_filter.process(context)

        # Pulse Intervals
        context = self.interval_builder.process(context)

        # Analysis Windows
        context = self.window_builder.process(context)

        # Metric Stability
        context = self.stability.process(context)

        context = self.source_pulse_extractor.process(context)

        context = self.periodicity_discovery.process(context)

        context = self.metric_segment_builder.process(context)

        context = self.metric_context_builder.process(context)

        context = self.metric_cluster_builder.process(context)

        context = self.domain_input_builder.build(context)

        if context.behaviour_profile is not None:

            context.behaviour_analytics_result = (
                self.behaviour_analytics_pipeline.analyze(
                    context.behaviour_profile,
                )
            )

            context.descriptor_set = (
                context.behaviour_analytics_result.descriptor_set
            )

            context.analytical_structure = (
                context.behaviour_analytics_result.analytical_structure
            )

            context.behaviour_descriptors = (
                context.descriptor_set.descriptors
            )

        return context
