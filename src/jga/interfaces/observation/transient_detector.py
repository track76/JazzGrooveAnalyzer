"""
=========================================================
Jazz Groove Analyzer (JGA)

Transient Detector Interface

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from jga.observation.signal_representation import SignalRepresentation
from jga.observation.transient import Transient


class TransientDetector(ABC):
    """
    Interface for transient detection algorithms.
    """

    @abstractmethod
    def detect(
        self,
        signal: SignalRepresentation,
    ) -> tuple[Transient, ...]:
        """
        Detect transient events from a signal representation.
        """
        raise NotImplementedError
