"""
=========================================================
Jazz Groove Analyzer (JGA)

Transient Detector

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from __future__ import annotations

import numpy as np

from jga.interfaces.observation.transient_detector import TransientDetector
from jga.observation.signal_representation import SignalRepresentation
from jga.observation.transient import Transient


class BasicTransientDetector(TransientDetector):
    """
    Basic transient detector based on the first-order discrete derivative.

    This implementation detects rapid signal variations by computing the
    absolute first derivative of the waveform and applying a threshold.
    """

    def __init__(self, threshold: float = 0.1):
        self._threshold = threshold

    def detect(
        self,
        signal: SignalRepresentation,
    ) -> tuple[Transient, ...]:

        derivative = np.abs(np.diff(signal.samples))

        indices = np.where(derivative >= self._threshold)[0] + 1

        return tuple(
            Transient(time=index / signal.sample_rate)
            for index in indices
        )
