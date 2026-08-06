from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_m80_multistem_analytical_score_content():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    score = context.analytical_score

    assert score is not None

    print()
    print("==============================")
    print("MULTISTEM ANALYTICAL SCORE")
    print("==============================")

    print(
        "Measures:",
        len(score.measures)
    )

    if score.measures:

        print(
            "First measure events:",
            len(
                score.measures[0].metric_events
            )
        )

        for event in (
            score.measures[0].metric_events[:20]
        ):
            print(
                event.source_name,
                event.beat_index,
                event.offset_ms,
            )

    print(
        "Instrument lanes:",
        len(
            score.instrument_lanes
        )
    )

    for lane in score.instrument_lanes:
        print(
            lane.name,
            len(
                lane.metric_events
            )
        )
