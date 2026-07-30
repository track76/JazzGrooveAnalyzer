import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.basic_feature_extractor import (
    BasicFeatureExtractor,
)
from jga.source_understanding.feature_name import (
    FeatureName,
)


def test_zero_crossing_rate_of_alternating_signal():

    extractor = BasicFeatureExtractor()

    stem = AudioStem(
        name="alternating",
        signal=np.array([1.0, -1.0, 1.0, -1.0]),
        sample_rate=4,
    )

    features = extractor.extract(stem)

    assert features.get(FeatureName.ZERO_CROSSING_RATE) == 1.0


def test_zero_crossing_rate_of_constant_signal():

    extractor = BasicFeatureExtractor()

    stem = AudioStem(
        name="constant",
        signal=np.ones(4),
        sample_rate=4,
    )

    features = extractor.extract(stem)

    assert features.get(FeatureName.ZERO_CROSSING_RATE) == 0.0
