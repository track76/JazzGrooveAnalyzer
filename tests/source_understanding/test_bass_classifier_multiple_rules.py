from jga.source_understanding.classifiers.bass_classifier import BassClassifier
from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet
from jga.source_understanding.instrument_family import InstrumentFamily


def test_bass_classifier_aggregates_multiple_rules():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 250.0)

    result = BassClassifier().classify(features)

    assert result.family is InstrumentFamily.BASS
    assert result.confidence > 0.5


def test_bass_classifier_reports_half_confidence_when_only_one_rule_matches():
    features = FeatureSet()

    features.set(FeatureName.SPECTRAL_CENTROID, 150.0)
    features.set(FeatureName.SPECTRAL_ROLLOFF, 800.0)

    result = BassClassifier().classify(features)

    assert result.family is InstrumentFamily.BASS
    assert result.confidence == 0.5
