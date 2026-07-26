from tests.support.domain_objects import make_metric_cluster

from jga.representation.builders.metric_cluster_portrait_builder import (
    MetricClusterPortraitBuilder,
)
from jga.representation.metric_cluster_portrait import (
    MetricClusterPortrait,
)


def test_builder_returns_metric_cluster_portrait():

    cluster = make_metric_cluster()

    builder = MetricClusterPortraitBuilder()

    portrait = builder.build(cluster)

    assert isinstance(
        portrait,
        MetricClusterPortrait,
    )


def test_builder_preserves_metric_cluster_reference():

    cluster = make_metric_cluster()

    portrait = (
        MetricClusterPortraitBuilder()
        .build(cluster)
    )

    assert portrait.metric_cluster is cluster


def test_builder_creates_one_metric_point_per_event():

    cluster = make_metric_cluster()

    portrait = (
        MetricClusterPortraitBuilder()
        .build(cluster)
    )

    assert len(portrait.points) == len(cluster.events)
