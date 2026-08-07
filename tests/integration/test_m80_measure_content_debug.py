from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


def test_m80_measure_content_debug():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    measure = context.reconstructed_measures[0]

    print()
    print("==============================")
    print("M80 CONTENT DEBUG")
    print("==============================")

    print(
        "Beat references:",
        len(measure.beat_references)
    )

    print(
        "Metric clusters:",
        len(measure.metric_clusters)
    )

    print(
        "Analytical events:",
        len(
            context.analytical_score
            .measures[0]
            .metric_events
        )
    )

