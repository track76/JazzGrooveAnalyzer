from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)


def test_visualization_output_keeps_scene_reference():

    scene = ScientificVisualizationScene()

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert output.scene is scene
