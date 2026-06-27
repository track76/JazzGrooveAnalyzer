"""
=========================================================
Jazz Groove Analyzer (JGA)

Dummy Separator

Author:
    Angelo Tracanna
=========================================================
"""

from jga.core.audio_stem import AudioStem
from jga.runtime.analysis_context import AnalysisContext

from jga.separation.base_separator import BaseSeparator


class DummySeparator(BaseSeparator):
    """
    Temporary separator.

    Creates one AudioStem using the complete mix.
    """

    def separate(
        self,
        context: AnalysisContext
    ) -> AnalysisContext:

        stem = AudioStem(
            name="Mix",
            signal=context.processed_audio,
            sample_rate=context.audio.sample_rate
        )

        context.audio_stems = [stem]

        context.log.add(
            "Dummy separator created 1 audio stem."
        )

        return context