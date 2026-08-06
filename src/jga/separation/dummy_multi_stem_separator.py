"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    dummy_multi_stem_separator.py

Description:
    Development separator generating logical ensemble
    sources for pipeline validation.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.audio_stem import AudioStem
from jga.core.audio_stem_collection import (
    AudioStemCollection,
)

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from jga.runtime.runtime_event import (
    RuntimeEvent,
)

from .base_separator import BaseSeparator


class DummyMultiStemSeparator(BaseSeparator):
    """
    Development separator.

    Creates multiple logical AudioStems from the same
    audio signal.

    No real source separation is performed.
    It validates the ensemble analysis pipeline.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        names = (
            "Bass",
            "Piano",
            "Ride",
            "Hi-Hat",
            "Snare",
            "Kick",
            "Trumpet",
        )

        stems = tuple(
            AudioStem(
                name=name,
                signal=context.processed_audio,
                sample_rate=context.audio.sample_rate,
                source="DummyMultiStemSeparator",
                confidence=0.5,
            )
            for name in names
        )

        context.audio_stems = AudioStemCollection(
            stems
        )

        context.log.add(
            RuntimeEvent(
                event_id="AUDIO_STEMS_CREATED",
                layer="SEPARATION",
                component="DummyMultiStemSeparator",
                message=(
                    "Dummy multi separator created "
                    "7 logical audio stems."
                ),
                input_type="SignalRepresentation",
                output_type="AudioStemCollection",
                metrics={
                    "stems": 7,
                },
            )
        )

        return context
