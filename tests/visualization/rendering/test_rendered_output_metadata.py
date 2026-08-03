from jga.visualization.rendered_output import (
    RenderedOutput,
)


def test_rendered_output_exposes_metadata():

    output = RenderedOutput(
        metadata={
            "format": "abstract",
        },
    )

    assert output.metadata == {
        "format": "abstract",
    }
