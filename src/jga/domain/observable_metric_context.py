"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    observable_metric_context.py

Description:
    Represents the observable metric context
    of an ensemble before metric projection.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ObservableMetricContext:
    """
    Represents the observable metric context
    identified from a musical performance.

    This object separates the physical time
    domain from the musical time domain.
    """

    observed_meter: str

    local_tempo: float

    confidence: float
