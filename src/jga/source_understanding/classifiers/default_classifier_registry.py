"""
=========================================================
Jazz Groove Analyzer (JGA)

Default Classifier Registry

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.source_understanding.classifiers.bass_classifier import (
    BassClassifier,
)
from jga.source_understanding.classifiers.chordal_classifier import (
    ChordalClassifier,
)
from jga.source_understanding.classifiers.classifier_registry import (
    ClassifierRegistry,
)
from jga.source_understanding.classifiers.percussion_classifier import (
    PercussionClassifier,
)
from jga.source_understanding.classifiers.voice_classifier import (
    VoiceClassifier,
)
from jga.source_understanding.classifiers.wind_classifier import (
    WindClassifier,
)


class DefaultClassifierRegistry(ClassifierRegistry):

    def __init__(self):

        super().__init__(
            classifiers=[
                BassClassifier(),
                PercussionClassifier(),
                WindClassifier(),
                ChordalClassifier(),
                VoiceClassifier(),
            ]
        )
