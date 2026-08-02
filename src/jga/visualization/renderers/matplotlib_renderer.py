"""
Matplotlib Renderer.

Concrete graphical renderer implementation.
"""

import matplotlib.pyplot as plt

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)

from jga.visualization.renderers.graphical_renderer import (
    GraphicalRenderer,
)


class MatplotlibRenderer(GraphicalRenderer):
    """
    Static scientific renderer.
    """

    def render(
        self,
        trajectory: VisualTrajectory,
    ):
        """
        Creates a scientific plot.
        """

        x_values = [
            point.x
            for point in trajectory.points
        ]

        y_values = [
            point.y
            for point in trajectory.points
        ]

        figure, axis = plt.subplots()

        axis.plot(
            x_values,
            y_values,
            marker="o",
        )

        axis.set_xlabel(
            "Temporal Order"
        )

        axis.set_ylabel(
            "Metric Temporal Displacement"
        )

        return figure
