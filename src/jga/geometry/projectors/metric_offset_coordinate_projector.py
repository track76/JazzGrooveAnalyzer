from jga.geometry.scientific_coordinate import (
    ScientificCoordinate,
)

from jga.interfaces.geometry import (
    ScientificCoordinateProjector,
)


class MetricOffsetCoordinateProjector(
    ScientificCoordinateProjector,
):
    """
    Projects Metric Offset into the X scientific coordinate.
    """

    def project(
        self,
        value: float,
    ) -> ScientificCoordinate:

        return ScientificCoordinate(
            name="Metric Offset",
            value=value,
            unit="ms",
        )
