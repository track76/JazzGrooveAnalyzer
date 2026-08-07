from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)

from jga.separation.dummy_multi_stem_separator import (
    DummyMultiStemSeparator,
)


def test_jga_val_001_metric_flow():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/validation/03 THE COST OF LIVING versione intro + 8 bar.mp3"
    )

    print("\n==============================")
    print("JGA-VAL-001 METRIC FLOW")
    print("==============================")

    print(
        "Beat References:",
        len(context.beat_references)
    )

    if context.beat_references:
        print(
            "First beat:",
            context.beat_references[0]
        )

        print(
            "Last beat:",
            context.beat_references[-1]
        )

    print(
        "Metric Clusters:",
        len(context.metric_clusters)
    )

    for index, cluster in enumerate(
        context.metric_clusters[:5]
    ):
        print(
            "Cluster",
            index,
            cluster
        )

    print(
        "Measures:",
        len(context.reconstructed_measures)
    )

    for measure in (
        context.reconstructed_measures
    ):
        print(
            "Measure:",
            measure.number,
            "start:",
            measure.start_time_seconds,
            "beats:",
            len(
                measure.beat_references
            )
        )
