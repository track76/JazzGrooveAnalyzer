from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_beat_reference_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("BEAT REFERENCE DEBUG")
    print("==============================")

    beats = context.beat_references[:10]

    for beat in beats:
        print(
            beat.index,
            beat.timestamp
        )
