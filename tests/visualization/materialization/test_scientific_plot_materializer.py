from jga.visualization.scientific_plot_materializer import (
    ScientificPlotMaterializer,
)


def test_scientific_plot_materializer_exists():

    materializer = ScientificPlotMaterializer()

    assert materializer is not None
