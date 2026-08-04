from jga.domain.services.beat_projection_engine import (
    BeatProjectionEngine,
)


def test_engine_can_be_instantiated():

    assert BeatProjectionEngine() is not None


def test_project_requires_arguments():

    engine = BeatProjectionEngine()

    try:
        engine.project()
        assert False
    except TypeError:
        pass


def test_empty_grid_returns_none():

    engine = BeatProjectionEngine()

    assert engine.project(
        event_timestamp=1.000,
        beat_grid=(),
    ) is None


def test_single_beat_projects_to_that_beat():

    engine = BeatProjectionEngine()

    beat = engine.project(
        event_timestamp=1.240,
        beat_grid=(
            1.000,
        ),
    )

    assert beat == 1.000


def test_projects_to_nearest_previous_beat():

    engine = BeatProjectionEngine()

    beat = engine.project(
        event_timestamp=1.740,
        beat_grid=(
            1.000,
            1.500,
            2.000,
        ),
    )

    assert beat == 1.500


def test_projects_to_nearest_following_beat():

    engine = BeatProjectionEngine()

    beat = engine.project(
        event_timestamp=1.870,
        beat_grid=(
            1.000,
            1.500,
            2.000,
        ),
    )

    assert beat == 2.000


def test_exact_beat_is_preserved():

    engine = BeatProjectionEngine()

    beat = engine.project(
        event_timestamp=1.500,
        beat_grid=(
            1.000,
            1.500,
            2.000,
        ),
    )

    assert beat == 1.500
