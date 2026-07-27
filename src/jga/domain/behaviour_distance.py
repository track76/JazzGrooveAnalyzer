from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BehaviourDistance:
    """
    Scientific comparison between two Behaviour Spaces.
    """

    physical_distance_ms: float

    metric_distance: float

    normalised_distance: float

    confidence: float

