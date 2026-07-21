from __future__ import annotations

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.descriptor_set import DescriptorSet


class DescriptorSetBuilder:
    """
    Builds the immutable DescriptorSet consumed by Behaviour Analytics.

    Scientific responsibility
    -------------------------

    Formalizes the transition

        BehaviourDescriptor*
                ↓
           DescriptorSet

    as defined by M-100 Descriptor Algebra.

    No analytical computation is performed here.

    This builder exists to make the transition between
    Behaviour Quantification and Behaviour Analytics
    explicit and fully traceable.
    """

    def build(
        self,
        descriptors: tuple[BehaviourDescriptor, ...],
    ) -> DescriptorSet:

        return DescriptorSet(
            descriptors=descriptors,
        )
