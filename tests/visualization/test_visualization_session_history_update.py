from jga.visualization.visualization_session import (
    VisualizationSession,
)

from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_visualization_session_appends_history_on_update():

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

    assert updated.history == (
        initial,
        updated.state,
    )

    assert session.history == (
        initial,
    )
