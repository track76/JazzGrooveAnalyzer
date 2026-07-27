from abc import ABC, abstractmethod

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


class ScientificCoordinateProjector(ABC):
    """
    Projects validated scientific quantities
    into geometric coordinates.
    """

    @abstractmethod
    def project(self, value: float) -> ScientificCoordinate:
        ...
