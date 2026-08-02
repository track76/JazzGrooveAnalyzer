"""
Visualization Projection Context.

M43.4

Carries all visualization exploration
parameters through the Visualization Layer.
"""

import pytest

from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)
from jga.visualization.visualization_projection_context import (
    VisualizationProjectionContext,
)


def test_context_preserves_projection_objects():

    temporal = TemporalVisualizationWindow(
        start_time=0.0,
        end_time=10.0,
    )

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=20.0,
        y_min=-5.0,
        y_max=5.0,
    )

    context = VisualizationProjectionContext(
        temporal_window=temporal,
        viewport=viewport,
    )

    assert context.temporal_window is temporal
    assert context.viewport is viewport


def test_context_is_immutable():

    context = VisualizationProjectionContext()

    with pytest.raises(Exception):
        context.viewport = None
