"""
Matplotlib Renderer.
"""

import matplotlib.pyplot as plt

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)


class MatplotlibRenderer:
    """
    Scientific matplotlib renderer.
    """

    def render(
        self,
        trajectory: VisualTrajectory,
    ):

        figure = plt.figure()

        axes = figure.add_subplot(111)

        if trajectory.points:

            axes.plot(
                [p.x for p in trajectory.points],
                [p.y for p in trajectory.points],
            )

        return figure

    def render_scene(
        self,
        scene: ScientificVisualizationScene,
    ):
        """
        Renders every trajectory contained
        in one scientific visualization scene.
        """

        figure = plt.figure()

        axes = figure.add_subplot(111)

        for descriptor in scene.trajectories:

            trajectory = descriptor.trajectory

            if trajectory.is_empty():
                continue

            axes.plot(
                [p.x for p in trajectory.points],
                [p.y for p in trajectory.points],
                label=descriptor.identifier,
            )

        if scene.trajectory_count() > 1:
            axes.legend()

        return figure
