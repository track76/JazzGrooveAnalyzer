"""
Plot Representation.

Represents the abstract structure
of a scientific plot.
"""

from dataclasses import dataclass, field

from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


@dataclass(frozen=True, slots=True)
class PlotRepresentation:
    """
    Scientific plot representation.

    Keeps traceability to the source
    rendered artifact and metadata.
    """

    source_artifact: RenderedVisualizationArtifact | None = None

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the plot representation.
        """

        return (
            self.source_artifact is not None
            and self.metadata is not None
        )
