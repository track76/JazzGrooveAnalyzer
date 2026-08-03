from jga.visualization.scientific_plot_generator import (
    ScientificPlotGenerator,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


def test_scientific_plot_generator_produces_representation():

    artifact = RenderedVisualizationArtifact()

    representation = (
        ScientificPlotGenerator()
        .generate(artifact)
    )

    assert isinstance(
        representation,
        PlotRepresentation,
    )
