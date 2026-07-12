"""
=========================================================
Jazz Groove Analyzer (JGA)

Basic Feature Extractor

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from __future__ import annotations

import numpy as np

from jga.interfaces.observation.feature_extractor import FeatureExtractor
from jga.observation.feature import Feature
from jga.observation.signal_representation import SignalRepresentation


class BasicFeatureExtractor(FeatureExtractor):
    """
    Basic feature extractor.

    This first implementation computes the signal energy and
    returns a Feature representing the observation time.
    """

    def extract(
        self,
        signal: SignalRepresentation,
    ) -> tuple[Feature, ...]:

        energy = np.sum(signal.samples ** 2)

        if energy <= 0:
            return ()

        return (Feature(time=0.0),)
