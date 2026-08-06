from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def test_m80_all_measure_clusters_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("==============================")
    print("ALL MEASURE CLUSTERS DEBUG")
    print("==============================")

    for measure in context.reconstructed_measures[:10]:
        print(
            "Measure",
            measure.number,
            "clusters",
            len(measure.metric_clusters),
        )
