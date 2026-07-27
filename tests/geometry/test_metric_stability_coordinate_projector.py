from jga.geometry.projectors import (
    MetricStabilityCoordinateProjector,
)


def test_metric_stability_projection():

    projector = MetricStabilityCoordinateProjector()

    coordinate = projector.project(
        0.85
    )

    assert coordinate.name == "Metric Stability"
    assert coordinate.value == 0.85
    assert coordinate.unit == "score"
