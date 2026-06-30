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

from jga.runtime.analysis_context import AnalysisContext


class SourcePulseExtractor:
    """
    JGA-232

    Builds SourcePulseSequence objects.

    Version 0.1
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        sequences = []

        # --------------------------------------------------
        # TODO
        #
        # When real source separation becomes available,
        # each AudioStem will produce one independent
        # SourcePulseSequence.
        #
        # Current implementation:
        # Dummy placeholder.
        # --------------------------------------------------

        context.source_pulse_sequences = sequences

        context.log.add(
            f"{len(sequences)} Source Pulse Sequences created."
        )

        return context