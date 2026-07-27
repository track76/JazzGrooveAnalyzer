from abc import ABC, abstractmethod

from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)

from jga.geometry.geometric_point import (
    GeometricPoint,
)


class ScientificGeometricProjectionBuilder(ABC):
    """
    Builds a scientific geometric plane
    from already validated geometric points.
    """

    @abstractmethod
    def build(
        self,
        points: tuple[GeometricPoint, ...],
    ) -> ScientificGeometricPlane:
        ...
