from __future__ import annotations

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)

from jga.domain.services.temporal_continuity_descriptor_builder import (
    TemporalContinuityDescriptorBuilder,
)


class BehaviourQuantificationBuilder:
    """
    Produces BehaviourDescriptors from a
    BehaviourQuantificationContext.

    Behaviour Quantification never modifies validated inputs.

    It derives deterministic BehaviourDescriptor objects from
    Behaviour representations and validated analytical inputs.
    """

    def __init__(self) -> None:

        self.temporal_continuity_builder = (
            TemporalContinuityDescriptorBuilder()
        )

    def build(
        self,
        context: BehaviourQuantificationContext,
    ) -> tuple[BehaviourDescriptor, ...]:

        descriptors: list[BehaviourDescriptor] = []

        for observation in (
            context.behaviour_profile.observations
        ):

            descriptors.append(
                self.temporal_continuity_builder.build(
                    observation,
                )
            )

        return tuple(descriptors)
