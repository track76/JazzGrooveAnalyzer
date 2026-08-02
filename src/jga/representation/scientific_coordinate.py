"""
Scientific Coordinate.

Representation Layer scientific quantity.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificCoordinate:
    """
    Immutable scientific coordinate.

    Coordinates represent scientific quantities,
    never graphical properties.
    """

    value: float

    unit: str

    dimension: str
