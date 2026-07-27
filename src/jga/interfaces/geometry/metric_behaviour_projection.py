from abc import ABC, abstractmethod

from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)


class MetricBehaviourProjection(ABC):
    """
    Builds scientific projection inputs
    from temporal musical observations.
    """

    @abstractmethod
    def project(
        self,
        event,
        beat_reference,
        stability_curve,
    ) -> ScientificProjectionInput:
        ...
