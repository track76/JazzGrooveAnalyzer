from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)

from jga.observation.default_behaviour_diagnostics import (
    DefaultBehaviourDiagnostics,
)


def test_default_behaviour_diagnostics_returns_result():

    frames = (
        BehaviourObservationFrame(
            time=0.0,
            physical_offset_ms=1.0,
            metric_offset=0.1,
            internal_bpm=120.0,
            stability=0.9,
        ),
    )

    result = DefaultBehaviourDiagnostics().analyze(
        frames
    )

    assert len(
        result.stable_regions.events
    ) == 1

    assert (
        result.stable_regions
        .events[0]
        .event_type
        == "stable_region"
    )

    assert len(
        result.scientific_evidence.evidences
    ) == 0
