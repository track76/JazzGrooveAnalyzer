from jga.visualization.scientific_plot_materializer import (
    ScientificPlotMaterializer,
)

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


def test_materialized_plot_is_valid():

    plot = (
        ScientificPlotMaterializer()
        .materialize(
            PlotRepresentation()
        )
    )

    assert plot.is_valid()
