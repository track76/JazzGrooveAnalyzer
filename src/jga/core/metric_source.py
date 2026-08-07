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
from uuid import UUID


@dataclass(slots=True)
class MetricSource:
    """
    One rhythmic source extracted from the audio.
    """

    name: str

    family: str

    confidence: float = 1.0

    source_id: UUID | None = None
