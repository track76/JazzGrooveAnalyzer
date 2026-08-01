from jga.domain.behaviour_observation_frame import (
    BehaviourObservationFrame,
)
from jga.observation.builders.behaviour_state_builder import (
    BehaviourStateBuilder,
)


def test_build_behaviour_state():

    frames = (
        BehaviourObservationFrame(
            time=0.0,
            physical_offset_ms=0.0,
            metric_offset=0.0,
            internal_bpm=120.0,
            stability=1.0,
        ),
    )

    state = BehaviourStateBuilder().build(
        frames=frames,
        start_index=0,
        end_index=0,
    )

    assert state.start_index == 0
    assert state.end_index == 0
    assert state.duration == 1
