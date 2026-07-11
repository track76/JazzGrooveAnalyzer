import numpy as np

from jga.observation.signal_representation import SignalRepresentation


def test_signal_representation_creation():
    samples = np.zeros(44100)

    signal = SignalRepresentation(
        samples=samples,
        sample_rate=44100,
    )

    assert signal.sample_rate == 44100
    assert len(signal.samples) == 44100
    assert signal.duration == 1.0