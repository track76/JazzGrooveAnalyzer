from jga.visualization.materialized_plot import (
    MaterializedPlot,
)


def test_materialized_plot_exists():

    plot = MaterializedPlot()

    assert plot is not None
