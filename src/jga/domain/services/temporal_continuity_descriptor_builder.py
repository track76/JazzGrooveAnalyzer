from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_observation import BehaviourObservation


class TemporalContinuityDescriptorBuilder:
    """
    Builder for the D-001 Temporal Continuity Descriptor.

    Mathematical specification:
        TemporalContinuity = C / N

    where:

        N = total number of Pulses in the BehaviourObservation

        C = number of Pulses belonging to the longest consecutive
            Pulse index sequence
    """

    def build(
        self,
        observation: BehaviourObservation,
    ) -> BehaviourDescriptor:

        value = self._compute_temporal_continuity(
            observation,
        )

        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="TemporalContinuity",
            value=value,
            provenance=self.__class__.__name__,
        )

    def _compute_temporal_continuity(
        self,
        observation: BehaviourObservation,
    ) -> float:

        pulses = observation.timeline.pulses

        if not pulses:
            raise ValueError(
                "BehaviourObservation must contain Pulses"
            )

        total = len(pulses)

        longest_sequence = 1
        current_sequence = 1

        previous_index = pulses[0].index

        for pulse in pulses[1:]:

            if pulse.index == previous_index + 1:
                current_sequence += 1

            else:
                current_sequence = 1

            if current_sequence > longest_sequence:
                longest_sequence = current_sequence

            previous_index = pulse.index

        return longest_sequence / total
