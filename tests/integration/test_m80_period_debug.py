from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_period_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("PERIOD DEBUG")
    print("==============================")

    beats = context.beat_references[:20]

    intervals = [
        b.timestamp - a.timestamp
        for a, b in zip(
            beats,
            beats[1:],
        )
    ]

    print(intervals)
    print(
        "average:",
        sum(intervals)/len(intervals)
    )
