import numpy as np

from jga.dsp.onset_detector import BasicOnsetDetector
from jga.observation.onset import Onset
from jga.observation.signal_representation import SignalRepresentation


def test_detect_returns_tuple():
    detector = BasicOnsetDetector()

    signal = SignalRepresentation(
        samples=np.zeros(2048),
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert isinstance(result, tuple)


def test_detect_empty_signal():
    detector = BasicOnsetDetector()

    signal = SignalRepresentation(
        samples=np.zeros(2048),
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert len(result) == 0


def test_detect_returns_onset_objects():
    detector = BasicOnsetDetector()

    samples = np.zeros(4096)
    samples[1024] = 1.0

    signal = SignalRepresentation(
        samples=samples,
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert all(isinstance(o, Onset) for o in result)
