"""
Graphic Renderer.

Domain contract for rendering a graphic scene.
"""

from dataclasses import dataclass

from jga.visualization.graphic_scene import (
    GraphicScene,
)

from jga.visualization.rendered_output import (
    RenderedOutput,
)


@dataclass(frozen=True, slots=True)
class GraphicRenderer:
    """
    Abstract renderer contract.
    """

    scene: GraphicScene | None = None

    def is_valid(
        self,
    ) -> bool:
        return True

    def render(
        self,
    ) -> RenderedOutput:
        """
        Produces rendered output.
        """

        return RenderedOutput(
            metadata=(
                self.scene.metadata
                if self.scene is not None
                else {}
            ),
        )
