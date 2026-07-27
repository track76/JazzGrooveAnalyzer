from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourChangeEvent:
    """
    Behavioural transition detected from
    Behaviour Observation Frames.
    """

    start_time: float

    end_time: float

    event_type: str

    intensity: float

