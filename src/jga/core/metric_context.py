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

from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.core.periodicity_segment import PeriodicitySegment
from jga.core.metric_segment import MetricSegment


@dataclass(frozen=True, slots=True)
class MetricContext:
    """
    Represents the complete observable Metric Context.

    The Metric Context is the terminal observable
    representation produced by the Observation Model.

    It contains no musical interpretation.

    It is the canonical observable representation
    consumed by the Translation Layer (τ₈).
    """

    source_pulse_sequences: tuple[SourcePulseSequence, ...]

    periodicity_segments: tuple[PeriodicitySegment, ...]

    metric_segments: tuple[MetricSegment, ...]

    def __post_init__(self) -> None:

        if not (
            self.source_pulse_sequences
            or self.periodicity_segments
            or self.metric_segments
        ):
            raise ValueError(
                "MetricContext requires observable evidence."
            )

    @property
    def segment_count(self) -> int:
        return len(self.metric_segments)
