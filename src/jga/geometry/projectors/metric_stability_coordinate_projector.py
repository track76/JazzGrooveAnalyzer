from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.interfaces.geometry import (
    ScientificCoordinateProjector,
)


class MetricStabilityCoordinateProjector(
    ScientificCoordinateProjector,
):
    """
    Projects Metric Stability score
    into the Y scientific coordinate.
    """

    def project(
        self,
        value: float,
    ) -> ScientificCoordinate:

        return ScientificCoordinate(
            name="Metric Stability",
            value=value,
            unit="score",
        )
