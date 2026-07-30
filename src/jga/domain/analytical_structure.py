from __future__ import annotations

from dataclasses import dataclass

from jga.domain.descriptor_set import DescriptorSet


@dataclass(slots=True, frozen=True)
class AnalyticalStructure:
    """
    Final analytical structure produced by Descriptor Algebra.

    This entity preserves the DescriptorSet resulting from the
    algebraic transformations. No analytical computation is
    performed here.
    """

    source_descriptor_set: DescriptorSet
