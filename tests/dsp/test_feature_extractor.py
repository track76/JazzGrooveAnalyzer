import numpy as np

from jga.dsp.feature_extractor import BasicFeatureExtractor
from jga.observation.feature import Feature
from jga.observation.signal_representation import SignalRepresentation


def test_extract_returns_tuple():
    extractor = BasicFeatureExtractor()

    signal = SignalRepresentation(
        samples=np.zeros(1024),
        sample_rate=44100,
    )

    result = extractor.extract(signal)

    assert isinstance(result, tuple)


def test_extract_empty_signal():
    extractor = BasicFeatureExtractor()

    signal = SignalRepresentation(
        samples=np.zeros(1024),
        sample_rate=44100,
    )

    result = extractor.extract(signal)

    assert len(result) == 0


def test_extract_returns_feature_objects():
    extractor = BasicFeatureExtractor()

    samples = np.zeros(1024)
    samples[512] = 1.0

    signal = SignalRepresentation(
        samples=samples,
        sample_rate=44100,
    )

    result = extractor.extract(signal)

    assert all(isinstance(f, Feature) for f in result)
