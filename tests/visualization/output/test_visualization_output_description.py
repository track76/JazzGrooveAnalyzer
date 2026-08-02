from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)


def test_visualization_output_has_description():

    scene = ScientificVisualizationScene()

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert output.description is not None
