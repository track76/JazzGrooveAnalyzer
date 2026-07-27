from dataclasses import dataclass

from .scientific_coordinate import ScientificCoordinate


@dataclass(frozen=True, slots=True)
class GeometricPoint:
    """
    Ordered collection of scientific coordinates representing
    one observable geometric point.
    """

    coordinates: tuple[ScientificCoordinate, ...]

    @property
    def dimension(self) -> int:
        return len(self.coordinates)
