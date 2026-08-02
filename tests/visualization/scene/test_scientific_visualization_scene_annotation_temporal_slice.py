from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_scene_slice_filters_annotations_by_window():

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="outside",
            ),
            VisualizationAnnotation(
                timestamp=20.0,
                label="inside",
            ),
            VisualizationAnnotation(
                timestamp=40.0,
                label="outside",
            ),
        ),
    )

    window = TemporalVisualizationWindow(
        start_time=15.0,
        end_time=25.0,
    )

    sliced = scene.slice(
        window,
    )

    assert sliced.annotations == (
        VisualizationAnnotation(
            timestamp=20.0,
            label="inside",
        ),
    )
