"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    stability_scorer.py

Description:
    Computes the Metric Stability Score.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np


class StabilityScorer:
    """
    JGA-159

    Computes the Metric Stability Score
    from PulseIntervals statistics.
    """

    def compute(
        self,
        durations: np.ndarray
    ) -> float:

        if len(durations) == 0:
            return 0.0

        mean = np.mean(durations)

        if mean == 0:
            return 0.0

        std = np.std(durations)

        cv = std / mean

        score = 1.0 / (1.0 + cv)

        return float(score)