from jga.geometry import (
    ScientificCoordinate,
    GeometricPoint,
    ScientificGeometricPlane,
    DefaultScientificGeometricPlaneBuilder,
)


def test_public_api():
    assert ScientificCoordinate
    assert GeometricPoint
    assert ScientificGeometricPlane
    assert DefaultScientificGeometricPlaneBuilder
