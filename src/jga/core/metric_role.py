"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_role.py

Description:
    Describes the metric role of one
    musical source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetricRole:
    """
    Metric role assigned to a musical source.
    """

    source_name: str

    periodicity_score: float

    mean_interval: float

    confidence: float

    is_metric: bool