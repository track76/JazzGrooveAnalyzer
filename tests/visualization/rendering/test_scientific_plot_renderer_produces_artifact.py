from jga.visualization.scientific_plot_renderer import (
    ScientificPlotRenderer,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_scientific_plot_renderer_produces_artifact():

    output = VisualizationOutput()

    artifact = (
        ScientificPlotRenderer()
        .render(output)
    )

    assert isinstance(
        artifact,
        RenderedVisualizationArtifact,
    )
