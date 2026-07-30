import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.basic_feature_extractor import (
    BasicFeatureExtractor,
)
from jga.source_understanding.feature_name import (
    FeatureName,
)


def test_rms_of_unit_signal():

    extractor = BasicFeatureExtractor()

    stem = AudioStem(
        name="unit",
        signal=np.array([1.0, -1.0, 1.0, -1.0]),
        sample_rate=4,
    )

    features = extractor.extract(stem)

    assert features.get(FeatureName.RMS) == 1.0


def test_rms_of_silence():

    extractor = BasicFeatureExtractor()

    stem = AudioStem(
        name="silence",
        signal=np.zeros(4),
        sample_rate=4,
    )

    features = extractor.extract(stem)

    assert features.get(FeatureName.RMS) == 0.0
