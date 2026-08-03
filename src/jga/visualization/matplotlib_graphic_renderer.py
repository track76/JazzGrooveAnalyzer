"""
Matplotlib Graphic Renderer.

Concrete renderer implementation.
"""

from dataclasses import dataclass

from matplotlib.figure import Figure

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

        figure = Figure()

        figure.add_subplot(111)

        return RenderedOutput(
            metadata={
                "renderer": "matplotlib",
                "type": "figure",
            },
            content=figure,
        )
