from unittest.mock import Mock

from jga.domain.metric_cluster import MetricCluster

from jga.geometry.builders import (
    DefaultScientificGeometricPlaneBuilder,
)


def make_cluster_mock():
    cluster = Mock(spec=MetricCluster)
    cluster.events = ()
    return cluster


def test_one_metric_cluster_produces_one_geometric_point():

    cluster = make_cluster_mock()

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build((cluster,))

    assert plane.size == 1


def test_two_metric_clusters_produce_two_geometric_points():

    cluster1 = make_cluster_mock()
    cluster2 = make_cluster_mock()

    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build(
        (
            cluster1,
            cluster2,
        )
    )

    assert plane.size == 2
