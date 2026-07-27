from dataclasses import dataclass

from .geometric_point import GeometricPoint


@dataclass(frozen=True, slots=True)
class ScientificGeometricPlane:
    """
    Collection of Geometric Points representing one scientific geometric plane.
    """

    points: tuple[GeometricPoint, ...]

    @property
    def size(self) -> int:
        return len(self.points)
