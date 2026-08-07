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
=========================================================
"""

from jga.audio.file_audio_source import FileAudioSource

from jga.engines.audio_preprocessor import AudioPreprocessor
from jga.engines.intro_detector import IntroDetector
from jga.engines.analysis_start_filter import AnalysisStartFilter

from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.engines.pulse_candidate_filter import PulseCandidateFilter
from jga.engines.pulse_builder import PulseBuilder
from jga.engines.analysis_window_builder import AnalysisWindowBuilder
from jga.engines.metric_stability_analyzer import MetricStabilityAnalyzer
from jga.engines.source_pulse_extractor import SourcePulseExtractor
from jga.engines.source_pulse_candidate_builder import (
    SourcePulseCandidateBuilder,
)
from jga.engines.domain_pulse_candidate_adapter import (
    DomainPulseCandidateAdapter,
)
from jga.engines.periodicity_discovery import PeriodicityDiscovery
from jga.engines.metric_segment_builder import MetricSegmentBuilder
from jga.engines.metric_context_builder import MetricContextBuilder
from jga.engines.metric_cluster_builder import MetricClusterBuilder
from jga.engines.ensemble_metric_consensus_engine import (
    EnsembleMetricConsensusEngine,
)

from jga.engines.ensemble_analysis_engine import (
    EnsembleAnalysisEngine,
)

from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.analysis_report import AnalysisReport

from jga.separation.null_separator import NullSeparator

from jga.source_understanding.pipeline import (
    SourceUnderstandingPipeline,
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
from jga.translation.dummy_semantic_bridge import (
    DummySemanticBridge,
)

from jga.domain.services.rule_based_behaviour_analytics_pipeline import (
    RuleBasedBehaviourAnalyticsPipeline,
)

from jga.domain.services.scientific_report_builder import (
    ScientificReportBuilder,
)

from jga.representation.pipeline import (
    RepresentationPipeline,
)

from jga.runtime.engines.scientific_geometry_engine_runner import (
    ScientificGeometryEngineRunner,
)

from jga.runtime.engines.scientific_behaviour_geometry_engine_runner import (
    ScientificBehaviourGeometryEngineRunner,
)

from jga.runtime.engines.behaviour_observation_runner import (
    BehaviourObservationRunner,
)

from jga.runtime.engines.reconstructed_measure_runner import (
    ReconstructedMeasureRunner,
)

from jga.runtime.engines.validation_dataset_runner import (
    ValidationDatasetRunner,
)

from jga.runtime.engines.analytical_score_runner import (
    AnalyticalScoreRunner,
)


class AnalysisPipeline:
    """
    Main JGA analysis pipeline.
    """

    def __init__(self, separator=None):

        self.loader = FileAudioSource()

        self.preprocessor = AudioPreprocessor()

        self.separator = (
            separator
            if separator is not None
            else NullSeparator()
        )

        self.source_understanding = SourceUnderstandingPipeline()

        self.intro_detector = IntroDetector()

        self.analysis_start_filter = AnalysisStartFilter()

        self.pulse_detector = PulseCandidateBuilder()

        self.pulse_filter = PulseCandidateFilter()

        self.interval_builder = PulseBuilder()

        self.window_builder = AnalysisWindowBuilder()

        self.stability = MetricStabilityAnalyzer()

        self.source_pulse_extractor = SourcePulseExtractor()

        self.source_pulse_candidate_builder = (
            SourcePulseCandidateBuilder()
        )

        self.domain_pulse_candidate_adapter = (
            DomainPulseCandidateAdapter()
        )

        self.periodicity_discovery = PeriodicityDiscovery()

        self.metric_segment_builder = MetricSegmentBuilder()

        self.metric_context_builder = MetricContextBuilder()

        self.metric_cluster_builder = MetricClusterBuilder()

        self.ensemble_metric_consensus = (
            EnsembleMetricConsensusEngine()
        )

        function_assigner = (
            RuleBasedMusicalFunctionAssignmentService()
        )

        contributor_assigner = (
            RuleBasedMetricContributorAssignmentService()
        )

        ensemble_pipeline = (
            RuleBasedEnsembleAnalysisPipeline(
                function_assigner=function_assigner,
                contributor_assigner=contributor_assigner,
            )
        )

        semantic_bridge = DummySemanticBridge()

        self.ensemble_analysis_engine = (
            EnsembleAnalysisEngine(
                semantic_bridge=semantic_bridge,
                ensemble_pipeline=ensemble_pipeline,
            )
        )

        self.domain_input_builder = (
            DefaultDomainInputBuilder(
                semantic_bridge=semantic_bridge,
                ensemble_pipeline=ensemble_pipeline,
            )
        )

        self.behaviour_analytics_pipeline = (
            RuleBasedBehaviourAnalyticsPipeline()
        )

        self.scientific_report_builder = (
            ScientificReportBuilder()
        )

        self.representation_pipeline = (
            RepresentationPipeline()
        )

        self.scientific_geometry_runner = (
            ScientificGeometryEngineRunner()
        )

        self.scientific_behaviour_geometry_runner = (
            ScientificBehaviourGeometryEngineRunner()
        )

        self.behaviour_observation_runner = (
            BehaviourObservationRunner()
        )

        self.reconstructed_measure_runner = (
            ReconstructedMeasureRunner()
        )

        self.validation_dataset_runner = (
            ValidationDatasetRunner()
        )

        self.analytical_score_runner = (
            AnalyticalScoreRunner()
        )

    def analyze(
        self,
        filepath: str,
    ) -> AnalysisContext:

        audio = self.loader.load(filepath)

        context = AnalysisContext(audio=audio)

        context.report = AnalysisReport(audio=audio)

        context.log.add("Audio loaded.")

        context = self.preprocessor.process(context)

        context = self.separator.process(context)

        source_result = (
            self.source_understanding.process(
                context.audio_stems
            )
        )

        context.observed_sources = (
            source_result.observed_sources
        )

        context.ensemble_profile = (
            source_result.ensemble_profile
        )

        context = self.pulse_detector.process(context)

        context = self.pulse_filter.process(context)

        context = self.interval_builder.process(context)

        context = self.window_builder.process(context)

        context = self.stability.process(context)

        intro = self.intro_detector.detect(
            context.stability_curve
        )

        context.analysis_start_time = (
            intro.analysis_start_time
        )

        context = self.analysis_start_filter.process(
            context
        )

        context.log.add(
            f"Analysis starts at {intro.analysis_start_time:.3f} s"
        )

        context = (
            self.source_pulse_candidate_builder.process(
                context
            )
        )

        context.domain_pulse_candidates = (
            self.domain_pulse_candidate_adapter.convert(
                context.source_pulse_sequences
            )
        )

        context = self.periodicity_discovery.process(context)

        context = self.metric_segment_builder.process(context)

        context = self.metric_context_builder.process(context)

        context = self.metric_cluster_builder.process(context)

        context = (
            self.ensemble_analysis_engine.process(
                context
            )
        )

        context.metric_contributors = (
            context.ensemble_analysis_result.metric_contributors
        )

        context = (
            self.ensemble_metric_consensus.process(
                context
            )
        )

        context = self.domain_input_builder.build(context)

        self.reconstructed_measure_runner.run(
            context,
        )

        self.scientific_behaviour_geometry_runner.run(
            context,
        )

        self.behaviour_observation_runner.run(
            context,
        )

        if context.behaviour_profile is not None:

            context.behaviour_analytics_result = (
                self.behaviour_analytics_pipeline.analyze(
                    context.behaviour_profile,
                    context.stability_curve,
                    context.behaviour_diagnostic_result,
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

            context.scientific_report = (
                self.scientific_report_builder.build(
                    context.behaviour_analytics_result,
                    context.behaviour_evolution_model,
                )
            )

        context.representation_result = (
            self.representation_pipeline.run(
                metric_clusters=context.metric_clusters,
            )
        )

        self.validation_dataset_runner.run(
            context,
        )

        self.analytical_score_runner.run(
            context,
        )

        return context
