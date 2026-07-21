from __future__ import annotations

from abc import ABC, abstractmethod

from jga.domain.analytical_structure import AnalyticalStructure
from jga.domain.descriptor_set import DescriptorSet


class DescriptorAlgebra(ABC):
    """
    Mathematical contract of M-100 Descriptor Algebra.

    Descriptor Algebra operates exclusively on immutable
    DescriptorSet objects.

    It derives analytical structures without modifying
    the original descriptors.

    Input
    -----
    DescriptorSet

    Output
    ------
    AnalyticalStructure
    """

    @abstractmethod
    def analyze(
        self,
        descriptor_set: DescriptorSet,
    ) -> AnalyticalStructure:
        """
        Performs a deterministic analytical transformation.
        """
        raise NotImplementedError
