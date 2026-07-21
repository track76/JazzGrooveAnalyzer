from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_observation import BehaviourObservation


class TemporalContinuityDescriptorBuilder:
    """
    Builds the D-001 Temporal Continuity descriptor.

    This initial implementation satisfies the scientific contract while
    deferring the mathematical formulation to a subsequent milestone.
    """

    def build(
        self,
        observation: BehaviourObservation,
    ) -> BehaviourDescriptor:
        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="TemporalContinuity",
            value=0.0,
            provenance=self.__class__.__name__,
        )
