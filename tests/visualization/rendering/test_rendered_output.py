from jga.visualization.rendered_output import (
    RenderedOutput,
)


def test_rendered_output_exists():

    output = RenderedOutput()

    assert output is not None
