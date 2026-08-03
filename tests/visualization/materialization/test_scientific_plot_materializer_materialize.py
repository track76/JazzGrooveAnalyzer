from jga.visualization.scientific_plot_materializer import (
    ScientificPlotMaterializer,
)

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


def test_scientific_plot_materializer_accepts_representation():

    representation = PlotRepresentation()

    result = (
        ScientificPlotMaterializer()
        .materialize(representation)
    )

    assert result is not None
