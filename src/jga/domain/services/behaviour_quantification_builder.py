from __future__ import annotations

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)

from jga.domain.services.behaviour_density_descriptor_builder import (
    BehaviourDensityDescriptorBuilder,
)

from jga.domain.services.metric_stability_descriptor_builder import (
    MetricStabilityDescriptorBuilder,
)

from jga.domain.services.temporal_continuity_descriptor_builder import (
    TemporalContinuityDescriptorBuilder,
)


class BehaviourQuantificationBuilder:
    """
    Produces BehaviourDescriptors from a
    BehaviourQuantificationContext.
    """

    def __init__(self) -> None:

        self.temporal_continuity_builder = (
            TemporalContinuityDescriptorBuilder()
        )

        self.metric_stability_builder = (
            MetricStabilityDescriptorBuilder()
        )

        self.behaviour_density_builder = (
            BehaviourDensityDescriptorBuilder()
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

            descriptors.append(
                self.behaviour_density_builder.build(
                    observation,
                )
            )

        descriptors.append(
            self.metric_stability_builder.build(
                context,
            )
        )

        return tuple(descriptors)
