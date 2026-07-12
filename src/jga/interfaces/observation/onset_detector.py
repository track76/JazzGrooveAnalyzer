"""
=========================================================
Jazz Groove Analyzer (JGA)

Onset Detector Interface

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from jga.observation.onset import Onset
from jga.observation.signal_representation import SignalRepresentation


class OnsetDetector(ABC):
    """
    Interface for onset detection algorithms.
    """

    @abstractmethod
    def detect(
        self,
        signal: SignalRepresentation,
    ) -> tuple[Onset, ...]:
        """
        Detect onset events from a signal representation.
        """
        raise NotImplementedError
