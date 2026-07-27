from jga.geometry.projectors import (
    MetricOffsetCoordinateProjector,
)


def test_metric_offset_projection():

    projector = MetricOffsetCoordinateProjector()

    coordinate = projector.project(
        12.5
    )

    assert coordinate.name == "Metric Offset"
    assert coordinate.value == 12.5
    assert coordinate.unit == "ms"
