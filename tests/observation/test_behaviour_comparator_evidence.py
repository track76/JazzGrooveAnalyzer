import pytest

from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.behaviour_comparator import (
    BehaviourComparator,
)


def test_comparator_preserves_evidence():

    left = BehaviourObservationFrame(
        time=0.0,
        physical_offset_ms=1.0,
        metric_offset=0.1,
        internal_bpm=120.0,
        stability=0.9,
    )

    right = BehaviourObservationFrame(
        time=1.0,
        physical_offset_ms=3.0,
        metric_offset=0.3,
        internal_bpm=121.0,
        stability=0.8,
    )

    comparator = BehaviourComparator()

    evidence = comparator.compare_with_evidence(
        left,
        right,
    )

    assert evidence is not None
    assert evidence.physical_offset_delta_ms == 2.0
    assert evidence.metric_offset_delta == pytest.approx(0.2)
    assert evidence.internal_bpm_delta == 1.0
    assert evidence.stability_delta == pytest.approx(-0.1)
