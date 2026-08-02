from jga.representation.metric_landscape import (
    MetricLandscape,
)

from jga.representation.representation_result import (
    RepresentationResult,
)

from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)


def test_source_visualization_builder():

    bass = MetricLandscape()

    result = RepresentationResult(
        metric_landscape=bass,
        metric_landscapes={
            "bass": bass,
        },
    )

    scene = (
        SourceVisualizationBuilder()
        .build(
            result,
            source="bass",
        )
    )

    assert scene.contains(
        "bass"
    )
