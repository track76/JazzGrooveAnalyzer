from dataclasses import FrozenInstanceError

import pytest

from jga.observation.transient import Transient


def test_transient_creation():
    transient = Transient(time=1.234)

    assert transient.time == 1.234


def test_transient_is_immutable():
    transient = Transient(time=1.234)

    with pytest.raises(FrozenInstanceError):
        transient.time = 2.0