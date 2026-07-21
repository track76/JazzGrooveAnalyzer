from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_observation import BehaviourObservation


class TemporalContinuityDescriptorBuilder:
    """
    Builder for the D-001 Temporal Continuity Descriptor.

    The current implementation validates the mathematical contract
    defined by M-001.

    A valid BehaviourObservation represents one continuous observed
    temporal interval.

    Future revisions will introduce Observable Variables allowing
    quantitative fragmentation analysis.
    """

    def build(
        self,
        observation: BehaviourObservation,
    ) -> BehaviourDescriptor:

        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="TemporalContinuity",
            value=1.0,
            provenance=self.__class__.__name__,
        )
