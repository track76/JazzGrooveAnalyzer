"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    metric_context.py

Description:
    Represents the complete observable Metric Context.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass

from jga.core.metric_segment import MetricSegment


@dataclass(frozen=True, slots=True)
class MetricContext:
    """
    Represents the complete observable Metric Context.

    The Metric Context is the coherent temporal organization
    emerging from the complete set of observed Metric Segments.

    It contains no musical interpretation.

    It is the canonical observable representation consumed by
    the Translation Layer (τ₈).
    """

    metric_segments: tuple[MetricSegment, ...]

    def __post_init__(self) -> None:
        if not self.metric_segments:
            raise ValueError(
                "MetricContext requires at least one MetricSegment."
            )

    @property
    def segment_count(self) -> int:
        return len(self.metric_segments)
