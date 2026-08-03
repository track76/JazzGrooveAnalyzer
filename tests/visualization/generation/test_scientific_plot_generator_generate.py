from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_scientific_plot_generator_accepts_artifact():

    artifact = RenderedVisualizationArtifact()

    result = (
        ScientificPlotGenerator()
        .generate(artifact)
    )

    assert result is not None
