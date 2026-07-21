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
from jga.domain.behaviour_observation import (
    BehaviourObservation,
)
from jga.domain.behaviour_profile import (
    BehaviourProfile,
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

    source_pulse_sequences: list | None = None

    # =====================================================
    # Pulse Detection
    # =====================================================

    pulse_candidates: list | None = None

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

    # =====================================================
    # Translation Layer τ₈
    # =====================================================

    ensemble_analysis_result: EnsembleAnalysisResult | None = None

    domain_pulse_candidates: tuple = ()

    elementary_metric_events: tuple = ()

    # =====================================================
    # Beat References
    # =====================================================

    beat_references: tuple[BeatReference, ...] = ()

    # =====================================================
    # Metric Clusters
    # =====================================================

    metric_clusters: tuple[MetricCluster, ...] = ()

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

    # =====================================================
    # Behaviour Analysis (M5)
    # =====================================================

    behaviour_observations: tuple[
        BehaviourObservation, ...
    ] = ()

    behaviour_profile: BehaviourProfile | None = None

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
