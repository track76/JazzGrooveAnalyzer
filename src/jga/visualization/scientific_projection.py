"""
Scientific Projection.

Visualization Layer transformation contract.

Transforms scientific representation into a
visualization-ready projection without changing
scientific meaning.
"""

from dataclasses import dataclass

from jga.representation.scientific_coordinate import (
    ScientificCoordinate,
)


@dataclass(frozen=True, slots=True)
class ScientificProjection:
    """
    Immutable visualization projection.

    Preserves the original scientific coordinate.
    """

    coordinate: ScientificCoordinate

    visual_value: float
