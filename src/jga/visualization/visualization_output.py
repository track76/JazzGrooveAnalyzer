"""
Visualization Output.

Represents a generated visualization artifact.
"""

from dataclasses import dataclass, field

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


@dataclass(frozen=True, slots=True)
class VisualizationOutput:
    """
    Generated visualization artifact.

    Keeps traceability to the source scene,
    identity description and metadata.
    """

    scene: ScientificVisualizationScene | None = None

    description: str = ""

    metadata: dict = field(
        default_factory=dict,
    )

    def is_valid(
        self,
    ) -> bool:
        """
        Checks structural validity
        of the visualization output.
        """

        return (
            self.scene is not None
            and bool(self.description)
            and self.metadata is not None
        )
