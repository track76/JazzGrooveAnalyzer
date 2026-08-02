from jga.representation.standard_coordinate_system import (
    DEFAULT_SCIENTIFIC_COORDINATE_SYSTEM,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


def test_default_coordinate_system_exists():

    assert (
        DEFAULT_SCIENTIFIC_COORDINATE_SYSTEM
        is not None
    )


def test_default_coordinate_system_contains_metric_axis():

    assert (
        DEFAULT_SCIENTIFIC_COORDINATE_SYSTEM
        .get_axis(
            "metric_temporal_displacement"
        )
        is METRIC_TEMPORAL_DISPLACEMENT_AXIS
    )
