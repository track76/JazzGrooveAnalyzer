"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    tau8_translator.py

Description:
    Implementation boundary of mathematical
    transformation τ₈.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from datetime import datetime
from uuid import uuid4

from jga.core.metric_context import MetricContext
from jga.domain.pulse_candidate import PulseCandidate
from jga.domain.sound_source import SoundSource


class Tau8Translator:
    """
    Software boundary implementing τ₈.

    τ₈ transforms the observable Metric Context
    into Domain PulseCandidate representations.

    It performs representation translation only.

    It does not:
    - create ElementaryMetricEvent;
    - assign MetricContributor;
    - introduce musical interpretation.
    """

    def translate(
        self,
        metric_context: MetricContext,
        sound_sources: tuple[SoundSource, ...],
    ) -> tuple[PulseCandidate, ...]:

        if metric_context is None:
            raise ValueError(
                "MetricContext cannot be None."
            )

        if sound_sources is None:
            raise ValueError(
                "SoundSources cannot be None."
            )

        candidates = []

        for sequence in metric_context.source_pulse_sequences:

            source = next(
                (
                    item
                    for item in sound_sources
                    if item.name == sequence.source.name
                ),
                None,
            )

            if source is None:
                raise ValueError(
                    f"No SoundSource found for MetricSource "
                    f"'{sequence.source.name}'."
                )

            for candidate in sequence.pulse_candidates:

                candidates.append(
                    PulseCandidate(
                        id=uuid4(),
                        sound_source_id=source.id,
                        timestamp=candidate.time,
                        confidence=candidate.confidence,
                        created_at=datetime.now(),
                    )
                )

        return tuple(candidates)
