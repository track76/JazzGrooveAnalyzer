from jga.representation.scientific_axis import (
    ScientificAxis,
)


def test_scientific_axis_type_exists():

    assert ScientificAxis is not None


def test_scientific_axis_preserves_semantics():

    axis = ScientificAxis(
        identifier="metric_temporal_displacement",
        name="Metric Temporal Displacement",
        dimension="metric_temporal_displacement",
        unit="milliseconds",
        description=(
            "Temporal displacement between "
            "ElementaryMetricEvent and BeatReference"
        ),
    )

    assert axis.identifier == (
        "metric_temporal_displacement"
    )

    assert axis.unit == "milliseconds"
