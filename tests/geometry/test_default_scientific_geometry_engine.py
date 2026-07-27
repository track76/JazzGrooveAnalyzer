from unittest.mock import Mock

from jga.domain.metric_cluster import MetricCluster
from jga.geometry.engines import (
    DefaultScientificGeometryEngine,
)
from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


def test_engine_projects_plane():
    engine = DefaultScientificGeometryEngine()

    cluster = Mock(spec=MetricCluster)

    plane = engine.project((cluster,))

    assert isinstance(
        plane,
        ScientificGeometricPlane,
    )

    assert plane.size == 1
