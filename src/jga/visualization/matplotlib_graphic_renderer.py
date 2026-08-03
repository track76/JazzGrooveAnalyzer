"""
Matplotlib Graphic Renderer.

Concrete renderer implementation.
"""

from dataclasses import dataclass

from jga.visualization.graphic_renderer import (
    GraphicRenderer,
)

from jga.visualization.rendered_output import (
    RenderedOutput,
)


@dataclass(frozen=True, slots=True)
class MatplotlibGraphicRenderer(
    GraphicRenderer,
):
    """
    Matplotlib based renderer.
    """

    def render(
        self,
    ) -> RenderedOutput:

        return RenderedOutput(
            metadata={
                "renderer": "matplotlib",
            },
            content={
                "type": "figure",
            },
        )
