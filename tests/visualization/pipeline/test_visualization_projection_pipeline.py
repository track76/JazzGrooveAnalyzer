from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)
from jga.visualization.projectors.temporal_visualization_projector import (
    TemporalVisualizationProjector,
)
from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


class IdentityProjector(
    TemporalVisualizationProjector,
):
    """
    Test projector.

    Performs no transformation.
    """

    def project(
        self,
        scene,
        window=None,
    ):
        return scene


def test_empty_pipeline_returns_original_scene():

    scene = ScientificVisualizationScene()

    pipeline = (
        VisualizationProjectionPipeline()
    )

    result = pipeline.project(
        scene,
    )

    assert result is scene


def test_pipeline_applies_projector():

    scene = ScientificVisualizationScene()

    pipeline = (
        VisualizationProjectionPipeline(
            projectors=(
                IdentityProjector(),
            ),
        )
    )

    result = pipeline.project(
        scene,
    )

    assert result is scene


def test_pipeline_accepts_multiple_projectors():

    scene = ScientificVisualizationScene()

    pipeline = (
        VisualizationProjectionPipeline(
            projectors=(
                IdentityProjector(),
                IdentityProjector(),
            ),
        )
    )

    result = pipeline.project(
        scene,
    )

    assert result is scene
