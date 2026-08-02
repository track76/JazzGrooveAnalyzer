from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_visualization_session_returns_current_state():

    state = VisualizationState()

    session = VisualizationSession(
        state=state,
    )

    assert session.current_state() == state
