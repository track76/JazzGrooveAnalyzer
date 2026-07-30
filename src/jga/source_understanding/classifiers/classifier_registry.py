"""
=========================================================
Jazz Groove Analyzer (JGA)

Classifier Registry

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


class ClassifierRegistry:
    """
    Executes all registered classifiers and
    returns the best InstrumentClassification.
    """

    def __init__(
        self,
        classifiers: list[InstrumentClassifier],
    ):
        self._classifiers = classifiers

    def classify(
        self,
        stem: AudioStem,
    ) -> InstrumentClassification:

        best = None

        for classifier in self._classifiers:

            result = classifier.classify(stem)

            if (
                best is None
                or result.confidence > best.confidence
            ):
                best = result

        return best
