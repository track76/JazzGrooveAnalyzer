"""
Multi Trajectory Renderer.

Visualization Layer renderer for multiple
identified visual trajectories.
"""

import matplotlib.pyplot as plt

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


class MultiTrajectoryRenderer:
    """
    Renders multiple identified visual trajectories.
    """

    def render(
        self,
        scene: ScientificVisualizationScene,
    ):
        """
        Creates a figure from multiple trajectories.
        """

        figure, axis = plt.subplots()

        for descriptor in scene.trajectories:

            trajectory = descriptor.trajectory

            x_values = [
                point.x
                for point in trajectory.points
            ]

            y_values = [
                point.y
                for point in trajectory.points
            ]

            axis.plot(
                x_values,
                y_values,
                marker="o",
                label=descriptor.identifier,
            )

        return figure
