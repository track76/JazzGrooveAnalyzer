from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


def test_metric_displacement_axis_has_scientific_meaning():

    axis = METRIC_TEMPORAL_DISPLACEMENT_AXIS

    assert (
        axis.identifier
        ==
        "metric_temporal_displacement"
    )

    assert axis.unit == "milliseconds"


def test_visualization_semantics_preserve_representation_boundary():

    assert (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
        .dimension
        ==
        "metric_temporal_displacement"
    )
