"""
Scientific Coordinate.

Representation Layer measured scientific quantity.
"""

from dataclasses import dataclass

from jga.representation.scientific_axis import (
    ScientificAxis,
)


@dataclass(frozen=True, slots=True)
class ScientificCoordinate:
    """
    Immutable scientific coordinate.

    A coordinate represents one measured value
    belonging to one ScientificAxis.

    Coordinates never contain graphical semantics.
    """

    axis: ScientificAxis

    value: float
