"""
=========================================================
Jazz Groove Analyzer (JGA)

Basic Feature Extractor

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.core.audio_stem import AudioStem

from jga.source_understanding.feature_extractor import (
    FeatureExtractor,
)
from jga.source_understanding.feature_set import (
    FeatureSet,
)


class BasicFeatureExtractor(FeatureExtractor):

    def extract(
        self,
        stem: AudioStem,
    ) -> FeatureSet:

        feature_set = FeatureSet()

        feature_set.set(
            "duration",
            len(stem.signal) / stem.sample_rate,
        )

        return feature_set
