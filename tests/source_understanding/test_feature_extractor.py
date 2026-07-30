import numpy as np
import pytest

from jga.core.audio_stem import AudioStem

from jga.source_understanding.feature_extractor import (
    FeatureExtractor,
)
from jga.source_understanding.feature_set import (
    FeatureSet,
)


class DummyFeatureExtractor(FeatureExtractor):

    def extract(self, stem: AudioStem) -> FeatureSet:

        feature_set = FeatureSet()
        feature_set.set("duration", 1.0)

        return feature_set


def test_feature_extractor_contract():

    extractor = DummyFeatureExtractor()

    stem = AudioStem(
        name="test",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    features = extractor.extract(stem)

    assert isinstance(features, FeatureSet)


def test_feature_extractor_is_abstract():

    with pytest.raises(TypeError):
        FeatureExtractor()
