"""
Source Visualization Builder.
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


class SourceVisualizationBuilder:
    """
    Builds a visualization scene from
    a selected representation source.
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
        source: str,
    ):

        trajectory = (
            self.adapter
            .adapt_source(
                result,
                source,
            )
        )

        return (
            self.scene_adapter
            .adapt(
                trajectory,
                identifier=source,
            )
        )
