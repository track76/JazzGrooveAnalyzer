import pytest

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_creates_valid_window():
    window = TemporalVisualizationWindow(
        start_time=10.0,
        end_time=25.0,
    )

    assert window.start_time == 10.0
    assert window.end_time == 25.0


def test_duration():
    window = TemporalVisualizationWindow(
        start_time=5.0,
        end_time=9.5,
    )

    assert window.duration == 4.5


def test_contains_start():
    window = TemporalVisualizationWindow(1.0, 5.0)

    assert window.contains(1.0)


def test_contains_middle():
    window = TemporalVisualizationWindow(1.0, 5.0)

    assert window.contains(3.0)


def test_contains_end():
    window = TemporalVisualizationWindow(1.0, 5.0)

    assert window.contains(5.0)


def test_does_not_contain_before():
    window = TemporalVisualizationWindow(1.0, 5.0)

    assert not window.contains(0.99)


def test_does_not_contain_after():
    window = TemporalVisualizationWindow(1.0, 5.0)

    assert not window.contains(5.01)


def test_rejects_negative_start_time():
    with pytest.raises(ValueError):
        TemporalVisualizationWindow(
            start_time=-1.0,
            end_time=5.0,
        )


def test_rejects_end_before_start():
    with pytest.raises(ValueError):
        TemporalVisualizationWindow(
            start_time=10.0,
            end_time=9.0,
        )


def test_is_immutable():
    window = TemporalVisualizationWindow(0.0, 1.0)

    with pytest.raises(Exception):
        window.start_time = 3.0
