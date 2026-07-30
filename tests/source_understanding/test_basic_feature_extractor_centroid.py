import numpy as np

from jga.core.audio_stem import AudioStem

from jga.source_understanding.basic_feature_extractor import (
    BasicFeatureExtractor,
)
from jga.source_understanding.feature_name import (
    FeatureName,
)


def test_spectral_centroid_of_440hz_sine():

    sample_rate = 44100

    duration = 1.0

    t = np.arange(
        int(sample_rate * duration)
    ) / sample_rate

    signal = np.sin(
        2 * np.pi * 440 * t
    )

    stem = AudioStem(
        name="440hz",
        signal=signal,
        sample_rate=sample_rate,
    )

    extractor = BasicFeatureExtractor()

    features = extractor.extract(stem)

    centroid = features.get(
        FeatureName.SPECTRAL_CENTROID
    )

    assert abs(centroid - 440.0) < 5.0
