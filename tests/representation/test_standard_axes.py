from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


def test_metric_temporal_displacement_axis_exists():

    assert (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
        is not None
    )


def test_metric_temporal_displacement_axis_semantics():

    axis = (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
    )

    assert axis.identifier == (
        "metric_temporal_displacement"
    )

    assert axis.unit == "milliseconds"
