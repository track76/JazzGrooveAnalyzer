"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    source_pulse_sequence.py

Description:
    Represents the sequence of rhythmic events
    extracted from a single metric source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from dataclasses import dataclass, field

from jga.core.metric_source import MetricSource
from jga.core.pulse_candidate import PulseCandidate


@dataclass(slots=True)
class SourcePulseSequence:
    """
    Rhythmic event sequence extracted
    from one observable Metric Source.

    The sequence preserves the identity
    of the originating MetricSource.
    """

    source: MetricSource

    pulse_candidates: list[PulseCandidate] = field(
        default_factory=list
    )

    @property
    def event_count(self) -> int:
        return len(self.pulse_candidates)
