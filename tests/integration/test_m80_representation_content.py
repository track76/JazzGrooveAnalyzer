from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_representation_content():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    result = context.representation_result

    assert result is not None

    print()
    print("==============================")
    print("REPRESENTATION DEBUG")
    print("==============================")

    landscape = result.metric_landscape

    print(
        "Landscape:",
        landscape is not None
    )

    if landscape:

        trajectory = (
            landscape.metric_trajectory
        )

        print(
            "Trajectory:",
            trajectory is not None
        )

        if trajectory:

            print(
                "Metric points:",
                len(
                    trajectory.metric_points
                )
            )

            for point in (
                trajectory.metric_points[:10]
            ):
                print(
                    point
                )
