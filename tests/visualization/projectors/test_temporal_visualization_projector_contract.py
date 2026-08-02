import pytest

from jga.visualization.projectors.temporal_visualization_projector import (
    TemporalVisualizationProjector,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


class DummyProjector(TemporalVisualizationProjector):
    def project(self, scene, window):
        return scene


def test_projector_is_instantiable_through_concrete_implementation():
    projector = DummyProjector()

    assert isinstance(projector, TemporalVisualizationProjector)


def test_project_returns_same_scene_instance():
    projector = DummyProjector()

    scene = object()

    window = TemporalVisualizationWindow(
        start_time=0.0,
        end_time=10.0,
    )

    result = projector.project(scene, window)

    assert result is scene


def test_project_accepts_temporal_window():
    projector = DummyProjector()

    scene = object()

    window = TemporalVisualizationWindow(
        start_time=5.0,
        end_time=15.0,
    )

    assert projector.project(scene, window) is scene
