from jga.representation.scientific_coordinate_system import (
    ScientificCoordinateSystem,
)

from jga.representation.standard_axes import (
    METRIC_TEMPORAL_DISPLACEMENT_AXIS,
)


def test_coordinate_system_contains_axes():

    system = ScientificCoordinateSystem(
        axes=(
            METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        )
    )

    assert (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
        in system.axes
    )


def test_coordinate_system_finds_axis_by_identifier():

    system = ScientificCoordinateSystem(
        axes=(
            METRIC_TEMPORAL_DISPLACEMENT_AXIS,
        )
    )

    axis = system.get_axis(
        "metric_temporal_displacement"
    )

    assert axis is (
        METRIC_TEMPORAL_DISPLACEMENT_AXIS
    )


def test_coordinate_system_returns_none_for_unknown_axis():

    system = ScientificCoordinateSystem()

    assert (
        system.get_axis("unknown")
        is None
    )


def test_coordinate_system_is_immutable():

    system = ScientificCoordinateSystem()

    try:
        system.axes = ()
        assert False
    except Exception:
        assert True
