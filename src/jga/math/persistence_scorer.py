"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    persistence_scorer.py

Description:
    Computes the Persistence Score of a
    rhythmic sequence.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

import numpy as np


class PersistenceScorer:
    """
    JGA-302

    Computes the Persistence Score.

    Version 0.1
    """

    def compute(
        self,
        intervals: np.ndarray
    ) -> float:

        if len(intervals) == 0:
            return 0.0

        score = min(
            len(intervals) / 16.0,
            1.0
        )

        return float(score)