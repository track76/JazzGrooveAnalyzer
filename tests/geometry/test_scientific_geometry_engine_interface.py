from inspect import isabstract

from jga.interfaces.representation import (
    ScientificGeometryEngine,
)


def test_engine_is_abstract():
    assert isabstract(ScientificGeometryEngine)


def test_engine_has_project():
    assert hasattr(ScientificGeometryEngine, "project")
