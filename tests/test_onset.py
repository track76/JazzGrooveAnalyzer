from dataclasses import FrozenInstanceError

import pytest

from jga.observation.onset import Onset


def test_onset_creation():
    onset = Onset(time=1.234)

    assert onset.time == 1.234


def test_onset_is_immutable():
    onset = Onset(time=1.234)

    with pytest.raises(FrozenInstanceError):
        onset.time = 2.0
