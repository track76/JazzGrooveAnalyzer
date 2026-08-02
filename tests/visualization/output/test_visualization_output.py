from jga.visualization.visualization_output import (
    VisualizationOutput,
)


def test_visualization_output_exists():

    output = VisualizationOutput()

    assert output is not None
