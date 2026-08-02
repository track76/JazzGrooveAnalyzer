from jga.visualization.renderers.matplotlib_renderer import (
    MatplotlibRenderer,
)

from jga.visualization.scientific_visualization_scene import (
    ScientificVisualizationScene,
)

from jga.visualization.visualization_annotation import (
    VisualizationAnnotation,
)


def test_renderer_accepts_scene_annotations():

    scene = ScientificVisualizationScene(
        annotations=(
            VisualizationAnnotation(
                timestamp=10.0,
                label="metric_event",
            ),
        ),
    )

    figure = (
        MatplotlibRenderer()
        .render_scene(
            scene,
        )
    )

    assert figure is not None
