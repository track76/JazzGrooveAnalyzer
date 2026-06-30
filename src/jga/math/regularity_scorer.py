"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    regularity_scorer.py

Description:
    Computes the Regularity Score of a
    rhythmic sequence.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np


class RegularityScorer:
    """
    JGA-301

    Computes the Regularity Score.

    Version 0.1
    """

    def compute(
        self,
        intervals: np.ndarray
    ) -> float:

        if len(intervals) < 2:
            return 0.0

        mean = np.mean(intervals)

        if mean == 0:
            return 0.0

        std = np.std(intervals)

        coefficient_of_variation = std / mean

        score = 1.0 / (1.0 + coefficient_of_variation)

        return float(np.clip(score, 0.0, 1.0))