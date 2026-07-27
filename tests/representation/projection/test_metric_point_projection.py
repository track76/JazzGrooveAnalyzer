"""
M14 — Scientific Geometric Projection

MetricPoint Projection Tests
"""

import pytest

from jga.representation.projection import ScientificProjectionEngine


def test_projection_engine_is_importable():
    assert ScientificProjectionEngine is not None


def test_projection_engine_can_be_instantiated():
    engine = ScientificProjectionEngine()
    assert engine is not None


def test_projection_not_implemented_yet():
    engine = ScientificProjectionEngine()

    with pytest.raises(NotImplementedError):
        engine.project(None)
