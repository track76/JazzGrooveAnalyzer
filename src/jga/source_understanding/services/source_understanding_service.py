from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.classifiers.dummy_instrument_classifier import (
    DummyInstrumentClassifier,
)
from jga.source_understanding.instrument_classifier import InstrumentClassifier
from jga.source_understanding.observed_source import ObservedSource
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


class SourceUnderstandingService:
    """
    Builds observed sources starting from separated audio stems.
    """

    def __init__(
        self,
        classifier: InstrumentClassifier | None = None,
    ) -> None:
        self._classifier = classifier or DummyInstrumentClassifier()

    def process(
        self,
        stems: AudioStemCollection,
    ) -> ObservedSourceCollection:
        observed = []

        for stem in stems:
            classification = self._classifier.classify(stem)

            observed.append(
                ObservedSource(
                    stem_id=stem.name,
                    classification=classification,
                )
            )

        return ObservedSourceCollection(tuple(observed))
