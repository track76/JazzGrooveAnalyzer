"""
Scientific Visualization Viewport Contract.

M43.1

A viewport defines the observable portion of a
ScientificVisualizationScene.

It does not modify scientific meaning.
"""

import pytest

from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)


def test_creates_valid_viewport():

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=100.0,
        y_min=-25.0,
        y_max=25.0,
    )

    assert viewport.x_min == 0.0
    assert viewport.x_max == 100.0
    assert viewport.y_min == -25.0
    assert viewport.y_max == 25.0


def test_rejects_invalid_x_range():

    with pytest.raises(ValueError):

        ScientificVisualizationViewport(
            x_min=10.0,
            x_max=5.0,
            y_min=-1.0,
            y_max=1.0,
        )


def test_rejects_invalid_y_range():

    with pytest.raises(ValueError):

        ScientificVisualizationViewport(
            x_min=0.0,
            x_max=10.0,
            y_min=5.0,
            y_max=-5.0,
        )


def test_viewport_is_immutable():

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=10.0,
        y_min=-5.0,
        y_max=5.0,
    )

    with pytest.raises(Exception):
        viewport.x_min = 1.0
