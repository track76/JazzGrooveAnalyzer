from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def test_m80_measure_clusters_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    measure = context.reconstructed_measures[0]

    print()
    print("==============================")
    print("MEASURE CLUSTERS DEBUG")
    print("==============================")

    print("clusters:", len(measure.metric_clusters))

    for index, cluster in enumerate(
        measure.metric_clusters
    ):
        print(
            index,
            cluster.beat_reference.index,
            cluster.beat_reference.timestamp
        )
