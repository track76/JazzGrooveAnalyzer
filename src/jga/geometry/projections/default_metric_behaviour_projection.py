from jga.domain.services.metric_offset_calculator import (
    MetricOffsetCalculator,
)

from jga.geometry.projectors import (
    MetricOffsetCoordinateProjector,
    MetricStabilityCoordinateProjector,
)

from jga.geometry.resolvers import (
    MetricStabilityResolver,
)

from jga.geometry.scientific_projection_input import (
    ScientificProjectionInput,
)


class DefaultMetricBehaviourProjection:
    """
    Builds scientific projection inputs
    from temporal musical observations.
    """

    def __init__(self):

        self.offset_calculator = (
            MetricOffsetCalculator()
        )

        self.offset_projector = (
            MetricOffsetCoordinateProjector()
        )

        self.stability_resolver = (
            MetricStabilityResolver()
        )

        self.stability_projector = (
            MetricStabilityCoordinateProjector()
        )

    def project(
        self,
        event,
        beat_reference,
        stability_curve,
    ) -> ScientificProjectionInput:

        offset = self.offset_calculator.compute(
            event,
            beat_reference,
        )

        offset_coordinate = (
            self.offset_projector.project(
                offset
            )
        )

        stability_point = (
            self.stability_resolver.resolve(
                event.timestamp,
                stability_curve,
            )
        )

        if stability_point is None:
            raise ValueError(
                "No stability point available."
            )

        stability_coordinate = (
            self.stability_projector.project(
                stability_point.score
            )
        )

        return ScientificProjectionInput(
            coordinates=(
                offset_coordinate,
                stability_coordinate,
            )
        )
