from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_analytical_score_content():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    score = context.analytical_score

    assert score is not None

    print()
    print("==============================")
    print("ANALYTICAL SCORE DEBUG")
    print("==============================")

    print(
        "Measures:",
        len(score.measures)
    )

    if score.measures:

        measure = score.measures[0]

        print(
            "First measure events:",
            len(measure.metric_events)
        )

        for event in (
            measure.metric_events[:10]
        ):
            print(
                event.source_name,
                event.beat_index,
                event.offset_ms,
            )
