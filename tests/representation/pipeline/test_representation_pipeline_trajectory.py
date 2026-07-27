from tests.support.domain_objects import make_metric_cluster

from jga.representation.pipeline import (
    RepresentationPipeline,
)


def test_representation_pipeline_creates_metric_trajectory():

    pipeline = RepresentationPipeline()

    result = pipeline.run(
        metric_clusters=(
            make_metric_cluster(),
        ),
    )

    assert result.metric_landscape.metric_trajectory is not None
