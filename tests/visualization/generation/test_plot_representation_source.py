from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_plot_representation_keeps_source_artifact():

    artifact = RenderedVisualizationArtifact()

    representation = (
        ScientificPlotGenerator()
        .generate(artifact)
    )

    assert representation.source_artifact is artifact
