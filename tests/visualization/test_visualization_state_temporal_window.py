from jga.visualization.visualization_state import (
    VisualizationState,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_visualization_state_supports_temporal_window():

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=20.0,
    )

    state = VisualizationState(
        temporal_window=window,
    )

    assert state.temporal_window == window
