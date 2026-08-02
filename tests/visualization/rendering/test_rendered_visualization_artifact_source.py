from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_rendered_artifact_keeps_source_output():

    output = VisualizationOutput()

    artifact = (
        ScientificPlotRenderer()
        .render(output)
    )

    assert artifact.source_output is output
