from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def test_m80_measure_clusters_debug():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert context.reconstructed_measures == ()
