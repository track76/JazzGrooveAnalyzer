from jga.visualization.visualization_state import (
    VisualizationState,
)


def test_visualization_state_supports_selected_sources():

    state = VisualizationState(
        selected_sources=(
            "bass",
            "piano",
        ),
    )

    assert state.selected_sources == (
        "bass",
        "piano",
    )
