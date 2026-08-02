from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_visualization_session_stores_initial_history():

    state = VisualizationState()

    session = VisualizationSession(
        state=state,
    )

    assert session.history == (
        state,
    )
