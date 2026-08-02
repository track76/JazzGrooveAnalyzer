from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


def test_pipeline_preserves_projector_order():

    calls = []

    class FirstProjector:

        def project(
            self,
            scene,
        ):

            calls.append("first")

            return scene

    class SecondProjector:

        def project(
            self,
            scene,
        ):

            calls.append("second")

            return scene

    scene = ScientificVisualizationScene()

    pipeline = (
        VisualizationProjectionPipeline(
            projectors=(
                FirstProjector(),
                SecondProjector(),
            ),
        )
    )

    result = pipeline.project(
        scene,
    )

    assert result is scene

    assert calls == [
        "first",
        "second",
    ]
