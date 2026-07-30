import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.basic_feature_extractor import (
    BasicFeatureExtractor,
)
from jga.source_understanding.feature_name import (
    FeatureName,
)
from jga.source_understanding.feature_set import (
    FeatureSet,
)


def test_basic_feature_extractor_returns_feature_set():

    extractor = BasicFeatureExtractor()

    stem = AudioStem(
        name="test",
        signal=np.zeros(1024),
        sample_rate=44100,
    )

    features = extractor.extract(stem)

    assert isinstance(features, FeatureSet)
    assert features.get(FeatureName.DURATION) is not None
