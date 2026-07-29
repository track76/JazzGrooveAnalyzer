from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import (
    BehaviourDescriptor,
)

from jga.domain.behaviour_observation import (
    BehaviourObservation,
)


class TemporalPersistenceDescriptorBuilder:
    """
    Builder for D-004 TemporalPersistence Descriptor.
    """

    def build(
        self,
        observation: BehaviourObservation,
    ) -> BehaviourDescriptor:

        observation_duration = (
            observation.last_pulse.timestamp
            -
            observation.first_pulse.timestamp
        )

        total_duration = (
            observation.timeline.last_pulse.timestamp
            -
            observation.timeline.first_pulse.timestamp
        )

        if total_duration <= 0:
            value = 1.0

        else:
            value = (
                observation_duration
                /
                total_duration
            )

        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="TemporalPersistence",
            value=value,
            provenance=self.__class__.__name__,
        )
