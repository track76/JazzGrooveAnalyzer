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

        axes = figure.add_subplot(111)

        if self.scene is not None and self.scene.layout is not None:

            axes.set_title(
                self.scene.layout.title,
            )

            axes.set_xlabel(
                self.scene.layout.x_axis,
            )

            axes.set_ylabel(
                self.scene.layout.y_axis,
            )

        return RenderedOutput(
            metadata={
                "renderer": "matplotlib",
                "type": "figure",
            },
            content=figure,
        )
