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
from jga.runtime.analysis_log import AnalysisLog
from jga.runtime.analysis_report import AnalysisReport
from jga.observation.signal_representation import SignalRepresentation


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

    elementary_metric_events: tuple = ()

    # =====================================================
    # Metric Clusters
    # =====================================================

    metric_clusters: list | None = None

    # =====================================================
    # Periodicity Discovery
    # =====================================================

    periodicity_segments: list | None = None

    # =====================================================
    # Analysis Log
    # =====================================================

    log: AnalysisLog = field(default_factory=AnalysisLog)
