from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


def test_visualization_session_projects_scene():

    session = VisualizationSession(
        state=VisualizationState(),
    )

    scene = ScientificVisualizationScene()

    projected = session.project(
        scene,
    )

    assert projected == scene
