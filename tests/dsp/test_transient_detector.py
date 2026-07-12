import numpy as np

from jga.dsp.transient_detector import BasicTransientDetector
from jga.observation.signal_representation import SignalRepresentation
from jga.observation.transient import Transient


def test_detect_returns_tuple():
    detector = BasicTransientDetector()

    signal = SignalRepresentation(
        samples=np.zeros(1024),
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert isinstance(result, tuple)


def test_detect_empty_signal():
    detector = BasicTransientDetector()

    signal = SignalRepresentation(
        samples=np.zeros(1024),
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert len(result) == 0


def test_detect_returns_transient_objects():
    detector = BasicTransientDetector()

    samples = np.zeros(1024)
    samples[512] = 1.0

    signal = SignalRepresentation(
        samples=samples,
        sample_rate=44100,
    )

    result = detector.detect(signal)

    assert all(isinstance(t, Transient) for t in result)
