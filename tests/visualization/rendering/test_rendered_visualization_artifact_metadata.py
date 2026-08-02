from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_rendered_artifact_exposes_metadata():

    artifact = (
        ScientificPlotRenderer()
        .render(
            VisualizationOutput()
        )
    )

    assert artifact.metadata is not None
