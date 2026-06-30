"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_contribution.py

Description:
    Represents the contribution of one
    metric source to an Ensemble Metric Event.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.metric_source import MetricSource


@dataclass(slots=True)
class MetricContribution:
    """
    Contribution of one metric source
    to an Ensemble Metric Event.
    """

    # Source producing the event
    source: MetricSource

    # Original onset time
    event_time: float

    # Reliability of this contribution
    confidence: float = 1.0