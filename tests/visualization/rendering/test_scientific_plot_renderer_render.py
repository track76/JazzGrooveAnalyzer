from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_scientific_plot_renderer_accepts_output():

    output = VisualizationOutput()

    renderer = ScientificPlotRenderer()

    result = (
        renderer
        .render(output)
    )

    assert result is not None
