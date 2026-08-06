from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_measure_alignment_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("MEASURE ALIGNMENT DEBUG")
    print("==============================")

    print(
        "Reconstructed measures:",
        len(
            context.reconstructed_measures
        )
    )

    for measure in (
        context.reconstructed_measures[:3]
    ):
        print(
            "Measure",
            measure.number,
            "beats:",
            len(
                measure.beat_references
            ),
            "start:",
            measure.start_time_seconds,
        )

    print(
        "Representation points:"
    )

    points = (
        context.representation_result
        .metric_landscape
        .metric_trajectory
        .metric_points
    )

    for point in points[:10]:
        print(
            point.event.timestamp,
            "beat",
            point.beat_reference.index,
        )
