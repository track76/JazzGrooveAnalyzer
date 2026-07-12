"""
=========================================================
Jazz Groove Analyzer (JGA)

Basic Onset Detector

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from __future__ import annotations

import librosa

from jga.interfaces.observation.onset_detector import OnsetDetector
from jga.observation.onset import Onset
from jga.observation.signal_representation import SignalRepresentation


class BasicOnsetDetector(OnsetDetector):
    """
    Basic onset detector using librosa.
    """

    def detect(
        self,
        signal: SignalRepresentation,
    ) -> tuple[Onset, ...]:

        onset_samples = librosa.onset.onset_detect(
            y=signal.samples,
            sr=signal.sample_rate,
            units="samples",
        )

        return tuple(
            Onset(time=sample / signal.sample_rate)
            for sample in onset_samples
        )
