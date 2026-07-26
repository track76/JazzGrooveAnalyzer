from tests.support.domain_objects import make_metric_cluster

from jga.representation.pipeline import RepresentationPipeline
from jga.representation.representation_result import (
    RepresentationResult,
)


def test_representation_pipeline_returns_result():

    pipeline = RepresentationPipeline()

    result = pipeline.run(
        metric_clusters=(make_metric_cluster(),),
    )

    assert isinstance(
        result,
        RepresentationResult,
    )


def test_representation_pipeline_creates_metric_landscape():

    pipeline = RepresentationPipeline()

    result = pipeline.run(
        metric_clusters=(make_metric_cluster(),),
    )

    assert result.metric_landscape is not None

    assert (
        len(
            result.metric_landscape.metric_cluster_portraits
        )
        == 1
    )
