"""
Scientific Plot Generator.

Responsible for creating scientific
plot representations.
"""

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)

from jga.visualization.plot_representation import (
    PlotRepresentation,
)


class ScientificPlotGenerator:
    """
    Scientific plot generator.
    """

    def generate(
        self,
        artifact: RenderedVisualizationArtifact,
    ) -> PlotRepresentation:
        """
        Generates a plot representation
        from a rendered visualization artifact.
        """

        return PlotRepresentation(
            source_artifact=artifact,
            metadata={},
        )
