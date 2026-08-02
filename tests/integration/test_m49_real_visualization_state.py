from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.visualization.source_visualization_builder import (
    SourceVisualizationBuilder,
)
from jga.visualization.pipeline.visualization_projection_pipeline import (
    VisualizationProjectionPipeline,
)
from jga.visualization.visualization_state import (
    VisualizationState,
)
from jga.visualization.temporal_visualization_window import (
    TemporalVisualizationWindow,
)


def test_m49_real_visualization_state():

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

    state = VisualizationState(
        temporal_window=TemporalVisualizationWindow(
            start_time=80.0,
            end_time=120.0,
        ),
        selected_sources=(
            "ensemble",
        ),
    )

    projected = (
        VisualizationProjectionPipeline()
        .project(
            scene,
            state=state,
        )
    )

    assert projected.contains(
        "ensemble"
    )

    assert projected.total_points() > 0
