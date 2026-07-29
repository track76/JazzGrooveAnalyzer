from __future__ import annotations

from jga.domain.descriptor_set import DescriptorSet

from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)

from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)


class DescriptorSpaceProjectionBuilder:
    """
    Converts BehaviourDescriptors into scientific coordinates.

    No mathematical transformation is applied.
    """

    def build(
        self,
        descriptor_set: DescriptorSet,
    ) -> ScientificProjectionInput:

        coordinates = tuple(
            ScientificCoordinate(
                name=descriptor.name,
                value=descriptor.value,
                unit="score",
            )
            for descriptor in descriptor_set
        )

        return ScientificProjectionInput(
            coordinates=coordinates,
        )
