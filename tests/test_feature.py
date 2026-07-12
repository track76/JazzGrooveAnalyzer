from dataclasses import FrozenInstanceError

import pytest

from jga.observation.feature import Feature


def test_feature_creation():
    feature = Feature(time=1.234)

    assert feature.time == 1.234


def test_feature_is_immutable():
    feature = Feature(time=1.234)

    with pytest.raises(FrozenInstanceError):
        feature.time = 2.0
