from jga.source_understanding.feature_name import FeatureName


def test_feature_name_enum():

    assert FeatureName.DURATION.value == "duration"
    assert FeatureName.RMS.value == "rms"
    assert FeatureName.ZERO_CROSSING_RATE.value == "zero_crossing_rate"
    assert FeatureName.SPECTRAL_CENTROID.value == "spectral_centroid"
    assert FeatureName.SPECTRAL_BANDWIDTH.value == "spectral_bandwidth"
    assert FeatureName.SPECTRAL_ROLLOFF.value == "spectral_rolloff"
