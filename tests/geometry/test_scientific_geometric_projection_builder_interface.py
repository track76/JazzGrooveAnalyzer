from inspect import isabstract

from jga.interfaces.geometry import (
    ScientificGeometricProjectionBuilder,
)


def test_projection_builder_is_abstract():

    assert isabstract(
        ScientificGeometricProjectionBuilder
    )


def test_projection_builder_has_build():

    assert hasattr(
        ScientificGeometricProjectionBuilder,
        "build",
    )
