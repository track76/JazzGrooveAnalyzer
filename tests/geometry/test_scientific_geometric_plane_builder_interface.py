from inspect import isabstract

from jga.interfaces.geometry import ScientificGeometricPlaneBuilder


def test_builder_is_abstract():
    assert isabstract(ScientificGeometricPlaneBuilder)


def test_builder_has_build():
    assert hasattr(ScientificGeometricPlaneBuilder, "build")
