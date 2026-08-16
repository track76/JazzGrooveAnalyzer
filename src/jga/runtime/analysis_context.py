"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_context.py

Description:
    Shared analysis context used by all JGA
    engines during the analysis pipeline.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

import numpy as np

from jga.core.audio_file import AudioFile
from jga.core.audio_stem_collection import AudioStemCollection

from jga.observation.signal_representation import SignalRepresentation

from jga.runtime.analysis_log import AnalysisLog
from jga.runtime.analysis_report import AnalysisReport

from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)

from jga.domain.beat_reference import BeatReference
from jga.domain.metric_cluster import MetricCluster
from jga.domain.pulse import Pulse
from jga.domain.internal_metric_timeline import (
    InternalMetricTimeline,
)
from jga.domain.internal_metric_signature import InternalMetricSignature
from jga.domain.declared_metric_reference import DeclaredMetricReference
from jga.domain.declared_metric_timeline import (
    DeclaredAnalysisScope,
    DeclaredQuarterPhaseOrigin,
)
from jga.domain.declared_meter import DeclaredMeter

from jga.domain.reconstructed_measure import (
    ReconstructedMeasure,
)
from jga.domain.behaviour_observation import (
    BehaviourObservation,
)
from jga.domain.behaviour_profile import (
    BehaviourProfile,
)

from jga.domain.behaviour_analytics_result import (
    BehaviourAnalyticsResult,
)

from jga.domain.behaviour_diagnostic_result import (
    BehaviourDiagnosticResult,
)

from jga.domain.behaviour_evolution_model import (
    BehaviourEvolutionModel,
)

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)

from jga.domain.descriptor_set import (
    DescriptorSet,
)

from jga.domain.analytical_structure import (
    AnalyticalStructure,
)

from jga.domain.scientific_report import (
    ScientificReport,
)

from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)

from jga.source_understanding.ensemble_profile import (
    EnsembleProfile,
)

from jga.validation.validation_dataset import (
    ValidationDataset,
)


@dataclass
class AnalysisContext:
    """
    Shared state used by all JGA engines
    during the analysis of a musical
    performance.
    """

    # =====================================================
    # Original Audio
    # =====================================================

    audio: AudioFile

    # =====================================================
    # Final Report
    # =====================================================

    report: AnalysisReport | None = None

    # =====================================================
    # Audio Processing
    # =====================================================

    processed_audio: np.ndarray | None = None

    signal_representation: SignalRepresentation | None = None

    audio_stems: AudioStemCollection | None = None


    # =====================================================
    # Source Understanding (M32)
    # =====================================================

    observed_sources: (
        ObservedSourceCollection | None
    ) = None

    ensemble_profile: EnsembleProfile | None = None
    source_pulse_sequences: list | None = None

    # =====================================================
    # Pulse Detection
    # =====================================================

    pulse_candidates: list | None = None

    candidate_period_population: object | None = None

    pulse_intervals: list | None = None

    # =====================================================
    # Window Analysis
    # =====================================================

    analysis_windows: list | None = None

    # =====================================================
    # Metric Stability
    # =====================================================

    stability_curve: object | None = None

    # =====================================================
    # Metric Segments
    # =====================================================

    metric_segments: list | None = None

    # =====================================================
    # Metric Context
    # =====================================================

    metric_context: object | None = None

    # Externally supplied musical context. It is not observation evidence.
    declared_metric_reference: DeclaredMetricReference | None = None

    declared_quarter_phase_origin: DeclaredQuarterPhaseOrigin | None = None

    declared_analysis_scope: DeclaredAnalysisScope | None = None

    declared_meter: DeclaredMeter | None = None

    # =====================================================
    # Translation Layer τ₈
    # =====================================================

    ensemble_analysis_result: EnsembleAnalysisResult | None = None

    domain_pulse_candidates: tuple = ()

    ensemble_metric_events: tuple = ()

    elementary_metric_events: tuple = ()

    elementary_metric_event_associations: tuple = ()

    metric_contributors: tuple = ()

    # =====================================================
    # Beat References
    # =====================================================

    beat_references: tuple[BeatReference, ...] = ()

    # =====================================================
    # Metric Clusters
    # =====================================================

    metric_clusters: tuple[MetricCluster, ...] = ()

    # =====================================================
    # Reconstructed Measures
    # =====================================================

    reconstructed_measures: tuple[
        ReconstructedMeasure, ...
    ] = ()

    # =====================================================
    # Pulses
    # =====================================================

    pulses: tuple[Pulse, ...] = ()

    # =====================================================
    # Internal Metric Timeline (τ₇)
    # =====================================================

    internal_metric_timeline: (
        InternalMetricTimeline | None
    ) = None

    internal_metric_signature: InternalMetricSignature | None = None

    # =====================================================
    # Behaviour Analysis (M5)
    # =====================================================

    behaviour_observations: tuple[
        BehaviourObservation, ...
    ] = ()

    behaviour_profile: BehaviourProfile | None = None

    # =====================================================
    # Behaviour Analytics (M6)
    # =====================================================

    behaviour_descriptors: tuple = ()

    semantics: tuple = ()

    descriptor_set: DescriptorSet | None = None

    analytical_structure: AnalyticalStructure | None = None

    scientific_report: ScientificReport | None = None

    behaviour_analytics_result: (
        BehaviourAnalyticsResult | None
    ) = None

    # =====================================================
    # Representation Layer (M13)
    # =====================================================

    representation_result: (
        RepresentationResult | None
    ) = None

    analytical_score: object | None = None

    # =====================================================
    # Scientific Validation Layer (M78)
    # =====================================================

    validation_dataset: (
        ValidationDataset | None
    ) = None

    # =====================================================
    # Scientific Geometry Layer (M17)
    # =====================================================

    scientific_geometric_plane: (
        ScientificGeometricPlane | None
    ) = None

    # =====================================================
    # Periodicity Discovery
    # =====================================================

    periodicity_segments: list | None = None

    # =====================================================
    # Analysis Log
    # =====================================================

    log: AnalysisLog = field(
        default_factory=AnalysisLog
    )

    # =====================================================
    # Behaviour Observation Layer (M18)
    # =====================================================

    behaviour_observation_frames: tuple = ()

    behaviour_change_events: tuple = ()

    behaviour_diagnostic_result: (
        BehaviourDiagnosticResult | None
    ) = None

    # =====================================================
    # Behaviour Evolution Layer (M28)
    # =====================================================

    behaviour_evolution_model: (
        BehaviourEvolutionModel | None
    ) = None
