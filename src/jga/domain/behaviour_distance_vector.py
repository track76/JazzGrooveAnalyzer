from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BehaviourDistanceVector:
    """
    Multidimensional scientific distance.

    Every component represents one observable
    behavioural dimension.
    """

    physical: float

    metric: float

    stability: float

    persistence: float

    regularity: float

