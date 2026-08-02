"""
Standard Scientific Coordinate System.

Canonical coordinate system definitions
for the Representation Layer.
"""

from jga.representation.scientific_coordinate_system import (
    ScientificCoordinateSystem,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


DEFAULT_SCIENTIFIC_COORDINATE_SYSTEM = (
    ScientificCoordinateSystem(
        axes=(
            METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        )
    )
)
