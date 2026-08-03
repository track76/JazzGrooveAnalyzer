from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_plot_representation_exposes_metadata():

    representation = (
        ScientificPlotGenerator()
        .generate(
            RenderedVisualizationArtifact()
        )
    )

    assert representation.metadata is not None
