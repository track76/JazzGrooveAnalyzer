from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)


def test_visualization_output_exposes_metadata():

    scene = ScientificVisualizationScene()

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert output.metadata is not None
