from jga.visualization.visualization_output_builder import (
    VisualizationOutputBuilder,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_visualization_output_builder_creates_output():

    scene = ScientificVisualizationScene()

    output = (
        VisualizationOutputBuilder()
        .build(scene)
    )

    assert isinstance(
        output,
        VisualizationOutput,
    )
