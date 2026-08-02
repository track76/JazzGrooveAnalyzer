from jga.representation.pipeline import (
    RepresentationPipeline,
)

from tests.factories.metric_cluster_factory import (
    make_metric_cluster,
)


def test_representation_pipeline_populates_metric_landscapes():

    result = (
        RepresentationPipeline()
        .run(
            metric_clusters=(
                make_metric_cluster(),
            ),
        )
    )

    assert "ensemble" in result.metric_landscapes

    assert (
        result.metric_landscapes["ensemble"]
        is result.metric_landscape
    )
