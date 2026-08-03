from jga.visualization.scientific_plot_materializer import (
    ScientificPlotMaterializer,
)

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


def test_materialized_plot_keeps_source_representation():

    representation = PlotRepresentation()

    plot = (
        ScientificPlotMaterializer()
        .materialize(representation)
    )

    assert plot.source_representation is representation
