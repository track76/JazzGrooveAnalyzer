from jga.source_understanding.classifiers.voice_classifier import (
    VoiceClassifier,
)
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_voice_classifier_identifies_voice_like_features():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 800.0)
    features.set(FeatureName.SPECTRAL_BANDWIDTH, 700.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 2000.0)
    features.set(FeatureName.DURATION, 3.0)

    result = VoiceClassifier().classify(features)

    assert result.family is InstrumentFamily.VOICE
    assert result.confidence > 0.0
