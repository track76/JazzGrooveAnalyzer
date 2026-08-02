from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_visualization_annotation_contract():

    annotation = VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
    )

    assert annotation.timestamp == 10.0

    assert annotation.label == "metric_event"
