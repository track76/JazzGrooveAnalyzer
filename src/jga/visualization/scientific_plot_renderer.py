"""
Scientific Plot Renderer.

Responsible for rendering scientific
visualization outputs.
"""

from jga.visualization.visualization_output import (
    VisualizationOutput,
)

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


class ScientificPlotRenderer:
    """
    Scientific visualization renderer.
    """

    def render(
        self,
        output: VisualizationOutput,
    ) -> RenderedVisualizationArtifact:

        return RenderedVisualizationArtifact(
            source_output=output,
            description=(
                "Rendered visualization artifact"
            ),
            metadata={},
        )
