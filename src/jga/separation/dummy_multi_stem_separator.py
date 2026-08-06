"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    dummy_multi_stem_separator.py

Description:
    Development separator producing multiple
    observable stems from one audio source.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import (
    AudioStemCollection,
)

from jga.runtime.analysis_context import AnalysisContext

from .base_separator import BaseSeparator


class DummyMultiStemSeparator(BaseSeparator):
    """
    Temporary multi-source separator.

    It does NOT perform source separation.

    It creates observable source placeholders
    required by higher JGA layers.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        names = (
            "Trumpet",
            "Piano",
            "Bass",
            "Ride",
            "Hi-Hat",
            "Snare",
            "Kick",
        )

        stems = tuple(
            AudioStem(
                name=name,
                signal=context.processed_audio,
                sample_rate=context.audio.sample_rate,
                source="DummyMultiStemSeparator",
                confidence=0.1,
            )
            for name in names
        )

        context.audio_stems = (
            AudioStemCollection(stems)
        )

        return context
