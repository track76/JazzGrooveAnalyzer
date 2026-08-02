from tests.support.domain_objects import (
    make_metric_cluster,
)

from jga.representation.pipeline import (
    RepresentationPipeline,
)

from jga.visualization.scientific_visualization_frame import (
    ScientificVisualizationFrame,
)


def test_visualization_frame_accepts_metric_landscape():

    result = (
        RepresentationPipeline()
        .run(
            metric_clusters=(
                make_metric_cluster(),
            )
        )
    )

    frame = ScientificVisualizationFrame(
        metric_landscape=(
            result.metric_landscape
        )
    )

    assert (
        frame.metric_landscape
        is result.metric_landscape
    )


def test_visualization_frame_preserves_representation_identity():

    result = (
        RepresentationPipeline()
        .run(
            metric_clusters=(
                make_metric_cluster(),
            )
        )
    )

    landscape = result.metric_landscape

    frame = ScientificVisualizationFrame(
        metric_landscape=landscape
    )

    assert frame.metric_landscape is landscape
