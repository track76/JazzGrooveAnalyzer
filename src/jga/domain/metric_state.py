"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_state.py

Description:
    Metric interpretation of one rhythmic behaviour.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from .metric_role import MetricRole


@dataclass
class MetricState:
    """
    Metric interpretation produced by the
    Metric Source Recognizer.
    """

    source_name: str

    role: MetricRole

    metric_evidence: float

    confidence: float