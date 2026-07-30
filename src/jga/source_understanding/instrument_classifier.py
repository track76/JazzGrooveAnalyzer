from abc import ABC, abstractmethod

from jga.source_understanding.instrument_classification import (
    InstrumentClassification,
)


class InstrumentClassifier(ABC):
    """
    Base interface for all instrument classifiers.

    Implementations may use machine learning, DSP,
    heuristics or external services.
    """

    @abstractmethod
    def classify(self, audio) -> InstrumentClassification:
        """
        Classify a sound source.

        Parameters
        ----------
        audio
            Audio representation of a single stem.

        Returns
        -------
        InstrumentClassification
        """
        raise NotImplementedError
