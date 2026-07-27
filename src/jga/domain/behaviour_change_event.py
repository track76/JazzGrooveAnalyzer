from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BehaviourChangeEvent:
    """
    Scientific observation of a behavioural transition.
    """

    start_time: float

    end_time: float

    event_type: str

    intensity: float

