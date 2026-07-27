from dataclasses import dataclass

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


@dataclass(frozen=True, slots=True)
class ScientificProjectionInput:
    """
    Collection of scientific coordinates
    ready for geometric projection.
    """

    coordinates: tuple[ScientificCoordinate, ...]
