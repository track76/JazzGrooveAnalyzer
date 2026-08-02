"""
Comparative Visualization Builder.
"""

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.visualization.metric_landscape_visualization_adapter import (
    MetricLandscapeVisualizationAdapter,
)

from jga.visualization.visual_trajectory_scene_adapter import (
    VisualTrajectorySceneAdapter,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


class ComparativeVisualizationBuilder:
    """
    Builds a visualization scene containing
    multiple selected sources.
    """

    def __init__(
        self,
    ):

        self.adapter = (
            MetricLandscapeVisualizationAdapter()
        )

        self.scene_adapter = (
            VisualTrajectorySceneAdapter()
        )

    def build(
        self,
        result: RepresentationResult,
        sources: tuple[str, ...],
    ) -> ScientificVisualizationScene:
        """
        Builds a comparative scene.
        """

        scenes = []

        for source in sources:

            trajectory = (
                self.adapter
                .adapt_source(
                    result,
                    source,
                )
            )

            scenes.append(
                self.scene_adapter
                .adapt(
                    trajectory,
                    identifier=source,
                )
            )

        current = scenes[0]

        for scene in scenes[1:]:

            current = current.merge(
                scene,
            )

        return current
