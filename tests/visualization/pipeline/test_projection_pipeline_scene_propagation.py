from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


class ReplacingProjector:

    def __init__(self):

        self.output = (
            ScientificVisualizationScene()
        )

    def project(
        self,
        scene,
    ):

        return self.output


class VerifyingProjector:

    def __init__(
        self,
        expected,
    ):

        self.expected = expected

    def project(
        self,
        scene,
    ):

        assert scene is self.expected

        return scene


def test_pipeline_propagates_projected_scene():

    first = ReplacingProjector()

    pipeline = (
        VisualizationProjectionPipeline(
            projectors=(
                first,
                VerifyingProjector(
                    first.output,
                ),
            ),
        )
    )

    pipeline.project(
        ScientificVisualizationScene(),
    )
