from jga.visualization.rendered_visualization_artifact import (
    RenderedVisualizationArtifact,
)


def test_rendered_visualization_artifact_exists():

    artifact = RenderedVisualizationArtifact()

    assert artifact is not None
