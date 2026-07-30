from __future__ import annotations

from abc import ABC, abstractmethod

from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)


class InstrumentClassifier(ABC):
    @abstractmethod
    def classify(
        self,
        features: FeatureSet,
    ) -> InstrumentClassification:
        """Classify an instrument using only the observed FeatureSet."""
        raise NotImplementedError
