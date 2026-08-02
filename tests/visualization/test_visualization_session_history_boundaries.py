from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_visualization_session_undo_does_not_cross_history_start():

    state = VisualizationState()

    session = VisualizationSession(
        state=state,
    )

    reverted = session.undo()

    assert reverted.current_state() == state


def test_visualization_session_redo_does_not_cross_history_end():

    session = VisualizationSession(
        state=VisualizationState(),
    )

    updated = session.update_state(
        temporal_window=TemporalVisualizationWindow(
            start_time=10.0,
            end_time=20.0,
        ),
    )

    restored = updated.redo()

    assert restored.current_state() == updated.state
