from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)
from jga.visualization.projectors.viewport_projector_adapter import (
    ViewportProjectorAdapter,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)
from jga.visualization.scientific_visualization_viewport import (
    ScientificVisualizationViewport,
)
from jga.visualization.visual_point import (
    VisualPoint,
)
from jga.visualization.visual_trajectory import (
    VisualTrajectory,
)
from jga.visualization.visualization_trajectory_descriptor import (
    VisualizationTrajectoryDescriptor,
)


def test_pipeline_applies_viewport_projector():

    scene = ScientificVisualizationScene(
        trajectories=(
            VisualizationTrajectoryDescriptor(
                identifier="bass",
                trajectory=VisualTrajectory(
                    points=(
                        VisualPoint(
                            x=0.0,
                            y=0.0,
                            time=0.0,
                        ),
                        VisualPoint(
                            x=5.0,
                            y=5.0,
                            time=1.0,
                        ),
                        VisualPoint(
                            x=20.0,
                            y=20.0,
                            time=2.0,
                        ),
                    ),
                ),
            ),
        ),
    )

    viewport = ScientificVisualizationViewport(
        x_min=0.0,
        x_max=10.0,
        y_min=0.0,
        y_max=10.0,
    )

    pipeline = VisualizationProjectionPipeline(
        projectors=(
            ViewportProjectorAdapter(
                viewport,
            ),
        ),
    )

    projected = pipeline.project(scene)

    assert (
        len(
            projected.trajectories[0]
            .trajectory.points
        )
        == 2
    )
