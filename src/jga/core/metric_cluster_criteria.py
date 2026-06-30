"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_cluster_criteria.py

Description:
    Defines the criteria used to recognize
    Metric Clusters.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetricClusterCriteria:
    """
    Parameters controlling Metric Cluster
    recognition.
    """

    # Minimum Stability Score
    minimum_stability: float = 0.70

    # Maximum allowed difference between
    # two consecutive Stability Scores.
    stability_tolerance: float = 0.05

    # Relative tolerance between the
    # average PulseIntervals of two windows.
    interval_tolerance: float = 0.03

    # Minimum consecutive windows required
    # to create a Metric Cluster.
    minimum_windows: int = 3