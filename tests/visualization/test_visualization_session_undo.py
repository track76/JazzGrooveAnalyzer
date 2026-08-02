from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_visualization_session_undo_moves_to_previous_state():

    initial = VisualizationState()

    session = VisualizationSession(
        state=initial,
    )

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=20.0,
    )

    updated = session.update_state(
        temporal_window=window,
    )

    reverted = updated.undo()

    assert reverted.current_state() == initial
