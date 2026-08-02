from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_rendered_artifact_is_valid():

    artifact = (
        ScientificPlotRenderer()
        .render(
            VisualizationOutput()
        )
    )

    assert artifact.is_valid()
