from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


class DummyProjectionPipeline:

    def __init__(self):
        self.called = False

    def project(
        self,
        scene,
        *,
        state,
    ):
        self.called = True
        return scene


def test_visualization_session_uses_injected_pipeline():

    pipeline = DummyProjectionPipeline()

    session = VisualizationSession(
        state=VisualizationState(),
        projection_pipeline=pipeline,
    )

    scene = ScientificVisualizationScene()

    session.project(
        scene,
    )

    assert pipeline.called
