from jga.source_understanding.feature_name import FeatureName
from jga.source_understanding.feature_set import FeatureSet


def test_feature_set_stores_features():

    feature_set = FeatureSet()

    feature_set.set(FeatureName.RMS, 0.12)
    feature_set.set(FeatureName.ZERO_CROSSING_RATE, 0.04)

    assert feature_set.get(FeatureName.RMS) == 0.12
    assert feature_set.get(FeatureName.ZERO_CROSSING_RATE) == 0.04


def test_feature_set_returns_none_for_missing_feature():

    feature_set = FeatureSet()

    assert feature_set.get(FeatureName.SPECTRAL_CENTROID) is None
