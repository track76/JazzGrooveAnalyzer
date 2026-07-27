from unittest.mock import Mock

from jga.domain.metric_cluster import MetricCluster
from jga.geometry.builders import (
    DefaultScientificGeometricPlaneBuilder,
)


def test_one_metric_cluster_produces_one_geometric_point():
    cluster = Mock(spec=MetricCluster)

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build((cluster,))

    assert plane.size == 1


def test_two_metric_clusters_produce_two_geometric_points():
    cluster1 = Mock(spec=MetricCluster)
    cluster2 = Mock(spec=MetricCluster)

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build(
        (
            cluster1,
            cluster2,
        )
    )

    assert plane.size == 2
