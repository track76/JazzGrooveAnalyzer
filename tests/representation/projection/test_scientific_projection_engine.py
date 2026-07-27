"""
Scientific Projection Engine

Behaviour Tests
"""

from jga.representation.projection import ScientificProjectionEngine
from jga.representation.metric_point import MetricPoint


def test_engine_exposes_project_method():
    engine = ScientificProjectionEngine()
    assert callable(engine.project)


def test_project_returns_metric_point():
    engine = ScientificProjectionEngine()

    point = engine.project(MetricPoint())

    assert isinstance(point, MetricPoint)


def test_projection_is_identity_until_geometry_is_defined():
    engine = ScientificProjectionEngine()

    point = MetricPoint()

    assert engine.project(point) is point
