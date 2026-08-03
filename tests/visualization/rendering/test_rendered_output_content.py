from jga.visualization.rendered_output import (
    RenderedOutput,
)


def test_rendered_output_exposes_content():

    output = RenderedOutput(
        content="abstract_render",
    )

    assert output.content == "abstract_render"
