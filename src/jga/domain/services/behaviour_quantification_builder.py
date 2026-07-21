from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_profile import BehaviourProfile
from jga.domain.services.temporal_continuity_descriptor_builder import (
    TemporalContinuityDescriptorBuilder,
)


class BehaviourQuantificationBuilder:
    """
    Produces the Behaviour Descriptors associated with one
    BehaviourProfile.

    Behaviour Quantification never modifies the BehaviourProfile.

    It derives deterministic BehaviourDescriptor objects from the
    validated Behaviour representation.
    """

    def __init__(self) -> None:

        self.temporal_continuity_builder = (
            TemporalContinuityDescriptorBuilder()
        )

    def build(
        self,
        profile: BehaviourProfile,
    ) -> tuple[BehaviourDescriptor, ...]:

        descriptors: list[BehaviourDescriptor] = []

        for observation in profile.observations:

            descriptors.append(
                self.temporal_continuity_builder.build(
                    observation,
                )
            )

        return tuple(descriptors)

