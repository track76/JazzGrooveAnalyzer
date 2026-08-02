from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)


def test_scientific_plot_renderer_exists():

    renderer = ScientificPlotRenderer()

    assert renderer is not None
