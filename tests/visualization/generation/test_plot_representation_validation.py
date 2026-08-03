from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_plot_representation_is_valid():

    representation = (
        ScientificPlotGenerator()
        .generate(
            RenderedVisualizationArtifact()
        )
    )

    assert representation.is_valid()
