"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    source_pulse_extractor.py

Description:
    Builds one SourcePulseSequence for each
    available Metric Source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.metric_source import MetricSource
from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.runtime.analysis_context import AnalysisContext
from jga.runtime.runtime_event import RuntimeEvent


class SourcePulseExtractor:
    """
    JGA-232

    Builds SourcePulseSequence objects.

    Version 0.3

    AD-015:
    MetricSource identity must originate from
    AudioStem identity.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        sequences = []

        if (
            context.pulse_candidates
            and context.audio_stems
        ):

            stem = context.audio_stems[0]

            sequence = SourcePulseSequence(
                source=MetricSource(
                    name=stem.name,
                    family="Unknown",
                ),
                pulse_candidates=list(
                    context.pulse_candidates
                ),
            )

            sequences.append(sequence)

        context.source_pulse_sequences = sequences

        context.log.add(
            RuntimeEvent(
                event_id="SOURCE_PULSE_SEQUENCES_CREATED",
                layer="ENGINE",
                component="SourcePulseExtractor",
                message=(
                    f"{len(sequences)} "
                    "Source Pulse Sequences created."
                ),
                input_type="list[PulseCandidate]",
                output_type="list[SourcePulseSequence]",
                metrics={
                    "source_pulse_sequences": len(sequences),
                },
            )
        )

        return context
