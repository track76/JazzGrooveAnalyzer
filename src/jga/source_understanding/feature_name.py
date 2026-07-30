"""
=========================================================
Jazz Groove Analyzer (JGA)

Feature Name

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from enum import Enum


class FeatureName(str, Enum):
    """
    Canonical names of observable audio features.
    """

    DURATION = "duration"

    RMS = "rms"

    ZERO_CROSSING_RATE = "zero_crossing_rate"

    SPECTRAL_CENTROID = "spectral_centroid"

    SPECTRAL_BANDWIDTH = "spectral_bandwidth"

    SPECTRAL_ROLLOFF = "spectral_rolloff"
