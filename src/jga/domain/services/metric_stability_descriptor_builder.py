from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from jga.domain.behaviour_descriptor import BehaviourDescriptor
from jga.domain.behaviour_quantification_context import (
    BehaviourQuantificationContext,
)


class MetricStabilityDescriptorBuilder:
    """
    Builder for the D-002 MetricStability Descriptor.

    The descriptor quantifies the validated Metric Stability
    produced by M4.

    It does not recompute metric stability.
    """

    def build(
        self,
        context: BehaviourQuantificationContext,
    ) -> BehaviourDescriptor:

        curve = context.stability_curve

        if not curve.points:
            value = 0.0

        else:
            value = (
                sum(
                    point.score
                    for point in curve.points
                )
                / len(curve.points)
            )

        return BehaviourDescriptor(
            id=uuid4(),
            created_at=datetime.now(),
            name="MetricStability",
            value=value,
            provenance=self.__class__.__name__,
        )
