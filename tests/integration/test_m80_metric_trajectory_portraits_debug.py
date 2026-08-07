from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_metric_trajectory_portraits_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    result = context.representation_result

    assert result is not None

    landscape = result.metric_landscape

    assert landscape is not None

    trajectory = landscape.metric_trajectory

    assert trajectory is not None

    print()
    print("==============================")
    print("TRAJECTORY PORTRAITS DEBUG")
    print("==============================")

    print(
        "Metric points:",
        len(
            trajectory.metric_points
        )
    )

    print(
        "Metric cluster portraits:",
        len(
            trajectory.metric_cluster_portraits
        )
    )

    for portrait in (
        trajectory.metric_cluster_portraits[:5]
    ):
        print(
            "Beat:",
            portrait.metric_cluster.beat_reference.index,
            "points:",
            len(portrait.points)
        )
