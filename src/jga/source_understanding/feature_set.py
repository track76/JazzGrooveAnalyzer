"""
=========================================================
Jazz Groove Analyzer (JGA)

Feature Set

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.source_understanding.feature_name import FeatureName


class FeatureSet:

    def __init__(self):

        self._features: dict[FeatureName, float] = {}

    def set(
        self,
        name: FeatureName,
        value: float,
    ) -> None:

        self._features[name] = value

    def get(
        self,
        name: FeatureName,
    ) -> float | None:

        return self._features.get(name)
