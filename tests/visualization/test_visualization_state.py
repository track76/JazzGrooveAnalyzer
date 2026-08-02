from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_visualization_state_contract():

    state = VisualizationState()

    assert state.selected_sources == ()

    assert state.active_annotations == ()

    assert state.view_mode == "default"
