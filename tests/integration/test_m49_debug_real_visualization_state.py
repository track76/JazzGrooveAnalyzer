from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)


def test_m49_debug_real_visualization_state():

    context = (
        AnalysisPipeline()
        .analyze(
            "recordings/III_Chet Baker - I fall in love too easily.mp3"
        )
    )

    scene = (
        SourceVisualizationBuilder()
        .build(
            context.representation_result,
            source="ensemble",
        )
    )

    trajectory = (
        scene.select("ensemble")
        .trajectory
    )

    print()
    print(
        "POINT COUNT:",
        len(trajectory.points),
    )

    if trajectory.points:
        print(
            "FIRST:",
            trajectory.points[0],
        )

        print(
            "LAST:",
            trajectory.points[-1],
        )

