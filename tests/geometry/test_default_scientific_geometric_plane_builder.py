from jga.geometry.builders import (
    DefaultScientificGeometricPlaneBuilder,
)
from jga.geometry.scientific_geometric_plane import (
    ScientificGeometricPlane,
)


def test_empty_metric_clusters():
    builder = DefaultScientificGeometricPlaneBuilder()

    plane = builder.build(())

    assert isinstance(plane, ScientificGeometricPlane)
    assert plane.size == 0
