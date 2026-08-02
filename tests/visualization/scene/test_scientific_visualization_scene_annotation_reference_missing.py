from uuid import uuid4

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)


def test_scene_returns_none_for_unknown_annotation_reference():

    scene = ScientificVisualizationScene()

    result = scene.annotation_for_reference(
        uuid4(),
    )

    assert result is None
