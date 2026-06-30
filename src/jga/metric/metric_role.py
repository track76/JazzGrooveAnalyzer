"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_role.py

Description:
    Metric role assumed by a musical source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from enum import Enum


class MetricRole(Enum):
    """
    Metric role currently assumed by a musical source.
    """

    METRIC = "Metric"

    NON_METRIC = "Non Metric"

    UNCERTAIN = "Uncertain"