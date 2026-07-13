"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    dummy_separator.py

Description:
    Temporary separator used during development.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import AudioStemCollection
from jga.runtime.analysis_context import AnalysisContext

from .base_separator import BaseSeparator


class NullSeparator(BaseSeparator):
    """
    Temporary separator.

    Creates one AudioStem containing the
    complete processed audio.
    """

    def process(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        stem = AudioStem(
            name="Mix",
            signal=context.processed_audio,
            sample_rate=context.audio.sample_rate,
            source="NullSeparator",
            confidence=1.0,
        )

        context.audio_stems = AudioStemCollection((stem,))

        context.log.add(
            "Dummy separator created 1 audio stem."
        )

        return context
