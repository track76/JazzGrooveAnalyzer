"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    analysis_report.py

Description:
    Collects all results produced during the analysis.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.audio_file import AudioFile
from jga.core.metric_cluster import MetricCluster
from jga.core.stability_curve import StabilityCurve
from jga.core.metric_segment import MetricSegment

@dataclass
class AnalysisReport:
    """
    Final report produced by the JGA pipeline.
    """

    # --------------------------------------------------
    # Audio Information
    # --------------------------------------------------

    audio: AudioFile

    # --------------------------------------------------
    # Basic Statistics
    # --------------------------------------------------

    pulse_candidates: int = 0

    pulse_intervals: int = 0

    analysis_windows: int = 0

    # --------------------------------------------------
    # Curves
    # --------------------------------------------------

    stability_curve: StabilityCurve | None = None

    # --------------------------------------------------
    # Musical Structures
    # --------------------------------------------------

    metric_segments: list[MetricSegment] | None = None

    metric_clusters: list[MetricCluster] | None = None

    # --------------------------------------------------
    # Audio Properties
    # --------------------------------------------------

    @property
    def duration(self) -> float:
        return self.audio.duration

    @property
    def filename(self) -> str:
        return self.audio.filename
