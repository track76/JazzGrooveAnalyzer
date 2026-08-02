from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_temporal_visualization_window_contract():

    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=30.0,
    )

    assert window.start_time == 10.0

    assert window.end_time == 30.0

    assert window.duration() == 20.0

    assert window.contains(
        15.0
    )

    assert not window.contains(
        5.0
    )
