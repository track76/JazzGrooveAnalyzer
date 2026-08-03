from jga.visualization.plot_representation import (
    PlotRepresentation,
)


def test_plot_representation_exists():

    representation = PlotRepresentation()

    assert representation is not None
