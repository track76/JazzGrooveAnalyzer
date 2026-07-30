"""
=========================================================
Jazz Groove Analyzer (JGA)

Chordal Classifier

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.audio_stem import AudioStem

from jga.source_understanding.instrument_classifier import (
    InstrumentClassifier,
)
from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)
from jga.source_understanding.instrument_family import (
    InstrumentFamily,
)


class ChordalClassifier(InstrumentClassifier):

    def classify(
        self,
        stem: AudioStem,
    ) -> InstrumentClassification:

        return InstrumentClassification(
            family=InstrumentFamily.UNKNOWN,
            instrument=None,
            confidence=0.0,
            classifier_name="ChordalClassifier",
            classifier_version="0.1",
        )
