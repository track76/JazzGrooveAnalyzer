from uuid import uuid4

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_visualization_annotation_supports_reference():

    reference = uuid4()

    annotation = VisualizationAnnotation(
        timestamp=10.0,
        label="metric_event",
        reference_id=reference,
    )

    assert annotation.reference_id == reference
