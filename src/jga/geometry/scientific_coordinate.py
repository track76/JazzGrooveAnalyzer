from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificCoordinate:
    """
    One validated scientific quantity.

    A ScientificCoordinate stores the result of a scientific
    measurement without performing any computation.
    """

    name: str
    value: float
    unit: str
