from __future__ import annotations

from abc import ABC, abstractmethod

from jga.geometry.scientific_behaviour_space import ScientificBehaviourSpace
from jga.geometry.scientific_geometric_plane import ScientificGeometricPlane


class ScientificBehaviourSpaceBuilder(ABC):

    @abstractmethod
    def build(
        self,
        plane: ScientificGeometricPlane,
    ) -> ScientificBehaviourSpace:
        ...
