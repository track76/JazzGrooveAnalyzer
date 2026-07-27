from inspect import isabstract

from jga.interfaces.geometry import (
    ScientificCoordinateProjector,
)


def test_projector_is_abstract():
    assert isabstract(
        ScientificCoordinateProjector
    )


def test_projector_has_project():
    assert hasattr(
        ScientificCoordinateProjector,
        "project",
    )
