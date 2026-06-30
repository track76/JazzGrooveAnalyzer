"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_source.py

Description:
    Represents one rhythmic source that can
    contribute to the Ensemble Metric Event.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetricSource:
    """
    One rhythmic source extracted from the audio.

    Examples:
        Ride
        Hi-Hat
        Kick
        Snare
        Brushes
        Double Bass
        Piano
        Guitar
    """

    name: str

    family: str

    confidence: float = 1.0