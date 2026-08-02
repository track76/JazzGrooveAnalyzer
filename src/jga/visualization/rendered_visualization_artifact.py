"""
Rendered Visualization Artifact.

Represents the result produced
by a visualization renderer.
"""

from dataclasses import dataclass, field

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


@dataclass(frozen=True, slots=True)
class RenderedVisualizationArtifact:
    """
    Rendered visualization result.

    Keeps traceability to the source
    visualization output and provides
    identity metadata.
    """

    source_output: VisualizationOutput | None = None

    description: str = ""

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the rendered artifact.
        """

        return (
            self.source_output is not None
            and bool(self.description)
            and self.metadata is not None
        )
