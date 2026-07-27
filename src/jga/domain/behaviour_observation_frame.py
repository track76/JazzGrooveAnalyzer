from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class BehaviourObservationFrame:
    """
    One scientific observation frame.
    """

    time: float

    physical_offset_ms: float

    metric_offset: float

    internal_bpm: float

    stability: float

