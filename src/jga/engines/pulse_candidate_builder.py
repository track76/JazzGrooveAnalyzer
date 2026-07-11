"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    pulse_candidate_detector.py

Purpose:
    Extract Pulse Candidates from the processed audio.

Input:
    AnalysisContext

Output:
    list[PulseCandidate]

Author:
    Angelo Tracanna

Copyright © 2026
=========================================================
"""

import librosa

from jga.core.pulse_candidate import PulseCandidate
from jga.runtime.analysis_context import AnalysisContext


class PulseCandidateBuilder:
    """
    JGA-130

    Estrae gli eventi audio che potrebbero
    appartenere alla pulsazione dell'ensemble.
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        audio = context.processed_audio

        sr = context.audio.sample_rate

        onset_frames = librosa.onset.onset_detect(
            y=audio,
            sr=sr,
            units="frames"
        )

        onset_strength = librosa.onset.onset_strength(
            y=audio,
            sr=sr
        )

        onset_times = librosa.frames_to_time(
            onset_frames,
            sr=sr
        )

        candidates = []

        for frame, time in zip(onset_frames, onset_times):

            strength = float(onset_strength[frame])

            candidates.append(
                PulseCandidate(
                    time=time,
                    strength=strength,
                    confidence=1.0
                )
            )

        # Aggiorna il contesto
        context.pulse_candidates = candidates

        # Aggiorna il report
        if context.report is not None:
            context.report.pulse_candidates = len(candidates)

        context.log.add(
            f"{len(candidates)} Pulse Candidates extracted."
        )

        return context