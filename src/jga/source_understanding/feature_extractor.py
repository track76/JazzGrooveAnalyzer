"""
=========================================================
Jazz Groove Analyzer (JGA)

Feature Extractor Contract

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from abc import ABC
from abc import abstractmethod

from jga.core.audio_stem import AudioStem

from jga.source_understanding.feature_set import FeatureSet


class FeatureExtractor(ABC):

    @abstractmethod
    def extract(
        self,
        stem: AudioStem,
    ) -> FeatureSet:
        """
        Extract observable features from an AudioStem.
        """
        ...
