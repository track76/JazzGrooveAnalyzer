from collections import Counter

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


def test_m80_events_per_source_debug():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    measure = context.analytical_score.measures[0]

    print()
    print("==============================")
    print("EVENTS PER SOURCE")
    print("==============================")

    print(
        Counter(
            event.source_name
            for event in measure.metric_events
        )
    )

    print()
    print("TOTAL:", len(measure.metric_events))
