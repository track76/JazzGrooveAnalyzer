"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    demucs_separator.py

Description:
    Demucs based source separation adapter.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from pathlib import Path
import tempfile

import librosa

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
from .demucs_runner import DemucsRunner


class DemucsSeparator(BaseSeparator):
    """
    Adapter between Demucs backend and JGA Core.

    Converts separated files into AudioStemCollection.
    """

    def __init__(
        self,
        runner=None,
    ):
        self.runner = (
            runner
            if runner is not None
            else DemucsRunner()
        )

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        with tempfile.TemporaryDirectory() as tmp:

            output = self.runner.separate(
                context.audio.path,
                Path(tmp),
            )

            stems = []

            for stem_file in sorted(
                output.glob("*.wav")
            ):

                signal, sample_rate = librosa.load(
                    stem_file,
                    sr=None,
                    mono=False,
                )

                stems.append(
                    AudioStem(
                        name=stem_file.stem,
                        signal=signal,
                        sample_rate=sample_rate,
                        source="DemucsSeparator",
                        confidence=1.0,
                    )
                )

            context.audio_stems = (
                AudioStemCollection(
                    tuple(stems)
                )
            )

            context.log.add(
                RuntimeEvent(
                    event_id="AUDIO_STEMS_CREATED",
                    layer="SEPARATION",
                    component="DemucsSeparator",
                    message=(
                        "Demucs separator created "
                        "audio stems."
                    ),
                    input_type="AudioFile",
                    output_type="AudioStemCollection",
                    metrics={
                        "stems": len(stems),
                    },
                )
            )

        return context
