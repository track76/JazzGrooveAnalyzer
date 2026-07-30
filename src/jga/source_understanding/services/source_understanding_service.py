from __future__ import annotations

from jga.core.audio_stem_collection import AudioStemCollection
from jga.source_understanding.basic_feature_extractor import BasicFeatureExtractor
from jga.source_understanding.classifiers.dummy_instrument_classifier import (
    DummyInstrumentClassifier,
)
from jga.source_understanding.observed_source import ObservedSource
from jga.source_understanding.observed_source_collection import (
    ObservedSourceCollection,
)


class SourceUnderstandingService:
    def __init__(
        self,
        classifier=None,
        feature_extractor=None,
    ):
        self._classifier = classifier or DummyInstrumentClassifier()
        self._feature_extractor = feature_extractor or BasicFeatureExtractor()

    def process(
        self,
        stems: AudioStemCollection,
    ) -> ObservedSourceCollection:
        observed_sources = []

        for stem in stems:
            features = self._feature_extractor.extract(stem)
            classification = self._classifier.classify(features)

            observed_sources.append(
                ObservedSource(
                    stem_id=stem.name,
                    classification=classification,
                )
            )

        return ObservedSourceCollection(tuple(observed_sources))
