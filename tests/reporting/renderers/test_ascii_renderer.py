from jga.reporting.renderers.ascii_renderer import (
    AnalyticalScoreAsciiRenderer,
)


def test_reporting_ascii_renderer_adapter_exists():
    """
    The Reporting layer no longer owns the ASCII rendering
    implementation.

    It only exposes a compatibility adapter that delegates
    to the canonical Visualization renderer.
    """

    renderer = AnalyticalScoreAsciiRenderer()

    assert renderer is not None

    assert hasattr(
        renderer,
        "_renderer",
    )
