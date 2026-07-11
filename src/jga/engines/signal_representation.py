"""
=========================================================
Jazz Groove Analyzer (JGA)

Signal Representation Engine

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SignalRepresentation:
    """
    Computational representation of an audio signal.

    This object belongs to the Observation Domain.
    It contains only observable acoustic information.
    """

    samples: np.ndarray
    sample_rate: int

    @property
    def duration(self) -> float:
        return len(self.samples) / self.sample_rate