from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_m80_first_measure_debug():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    measure = (
        context.analytical_score.measures[0]
    )

    print()
    print("==============================")
    print("FIRST MEASURE DEBUG")
    print("==============================")

    for event in measure.metric_events:
        print(
            event.source_name,
            "position=",
            event.theoretical_position,
            "beat=",
            event.beat_index,
            "offset=",
            event.offset_ms,
        )
