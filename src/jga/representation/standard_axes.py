"""
Standard Scientific Axes.

Canonical scientific axis definitions
for the Representation Layer.
"""

from jga.representation.scientific_axis import (
    ScientificAxis,
)


METRIC_TEMPORAL_DISPLACEMENT_AXIS = ScientificAxis(
    identifier="metric_temporal_displacement",
    name="Metric Temporal Displacement",
    dimension="metric_temporal_displacement",
    unit="milliseconds",
    description=(
        "Temporal displacement between "
        "ElementaryMetricEvent and BeatReference"
    ),
)
