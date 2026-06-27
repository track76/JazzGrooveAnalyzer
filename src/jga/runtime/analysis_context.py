"""
=========================================================
Jazz Groove Analyzer (JGA)

Analysis Context

Author:
    Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass, field
import numpy as np

from jga.core.audio_file import AudioFile
from jga.runtime.analysis_log import AnalysisLog


@dataclass
class AnalysisContext:
    """
    Shared state used by all JGA engines during
    the analysis of a musical performance.
    """

    # Original audio loaded from disk
    audio: AudioFile

    # Audio after preprocessing
    processed_audio: np.ndarray | None = None

    # Audio stems
    audio_stems: list | None = None

    # Pulse Candidates
    pulse_candidates: list | None = None

    # Pulse Intervals
    pulse_intervals: list | None = None

    analysis_windows: list | None = None

    stability_curve: object | None = None

    # Analysis log
    log: AnalysisLog = field(default_factory=AnalysisLog)