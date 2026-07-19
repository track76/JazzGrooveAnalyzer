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

from jga.core.source_pulse_sequence import SourcePulseSequence
from jga.core.metric_source import MetricSource
from jga.runtime.analysis_context import AnalysisContext


class SourcePulseExtractor:
    """
    JGA-232

    Builds SourcePulseSequence objects.

    Version 0.2
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        sequences = []

        if context.pulse_candidates:

            sequence = SourcePulseSequence(
                source=MetricSource(
                    name="mix",
                    family="Unknown",
                ),
                pulse_candidates=list(context.pulse_candidates),
            )

            sequences.append(sequence)

        context.source_pulse_sequences = sequences

        context.log.add(
            f"{len(sequences)} Source Pulse Sequences created."
        )

        return context
