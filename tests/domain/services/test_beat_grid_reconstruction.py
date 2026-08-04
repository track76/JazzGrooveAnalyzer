from jga.domain.services.beat_grid_reconstructor import (
    BeatGridReconstructor,
)


def test_reconstructor_can_be_instantiated():

    assert BeatGridReconstructor() is not None


def test_empty_seed_sequence_returns_empty_tuple():

    reconstructor = BeatGridReconstructor()

    assert reconstructor.reconstruct(
        (),
        period=0.500,
    ) == ()


def test_regular_seed_sequence_is_preserved():

    reconstructor = BeatGridReconstructor()

    seeds = (
        1.000,
        1.500,
        2.000,
    )

    grid = reconstructor.reconstruct(
        seeds,
        period=0.500,
    )

    assert grid == seeds


def test_grid_reconstruction_preserves_seed_order():

    reconstructor = BeatGridReconstructor()

    seeds = (
        2.000,
        1.000,
        1.500,
    )

    grid = reconstructor.reconstruct(
        seeds,
        period=0.500,
    )

    assert grid == (
        1.000,
        1.500,
        2.000,
    )


def test_grid_contains_unique_beats():

    reconstructor = BeatGridReconstructor()

    seeds = (
        1.000,
        1.500,
        1.500,
        2.000,
    )

    grid = reconstructor.reconstruct(
        seeds,
        period=0.500,
    )

    assert grid == (
        1.000,
        1.500,
        2.000,
    )


def test_grid_regularizes_small_seed_deviations():

    reconstructor = BeatGridReconstructor()

    seeds = (
        1.000,
        1.530,
        2.010,
    )

    grid = reconstructor.reconstruct(
        seeds,
        period=0.505,
    )

    assert grid == (
        1.000,
        1.505,
        2.010,
    )


def test_grid_regularizes_small_seed_deviations():

    reconstructor = BeatGridReconstructor()

    seeds = (
        1.000,
        1.530,
        2.010,
    )

    grid = reconstructor.reconstruct(
        seeds,
        period=0.505,
    )

    assert grid == (
        1.000,
        1.505,
        2.010,
    )
