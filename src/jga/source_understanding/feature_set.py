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


class FeatureSet:

    def __init__(self):

        self._features: dict[str, float] = {}

    def set(
        self,
        name: str,
        value: float,
    ) -> None:

        self._features[name] = value

    def get(
        self,
        name: str,
    ) -> float | None:

        return self._features.get(name)
