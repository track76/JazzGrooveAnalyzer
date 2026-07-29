from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import (
    BehaviourDescriptor,
)

from jga.domain.behaviour_observation import (
    BehaviourObservation,
)


class BehaviourDensityDescriptorBuilder:
    """
    Builder for D-003 BehaviourDensity Descriptor.
    """

    def build(
        self,
        observation: BehaviourObservation,
    ) -> BehaviourDescriptor:

        pulses = len(
            observation.timeline.pulses
        )

        duration = (
            observation.last_pulse.timestamp
            -
            observation.first_pulse.timestamp
        )

        value = (
            pulses / (pulses + duration)
            if pulses > 0
            else 0.0
        )

        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="BehaviourDensity",
            value=value,
            provenance=self.__class__.__name__,
        )
