from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m80_metric_cluster_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("METRIC CLUSTER DEBUG")
    print("==============================")

    print(
        "Clusters:",
        len(context.metric_clusters)
    )

    for cluster in context.metric_clusters[:10]:

        print(
            cluster.beat_reference.index,
            cluster.beat_reference.timestamp
        )
