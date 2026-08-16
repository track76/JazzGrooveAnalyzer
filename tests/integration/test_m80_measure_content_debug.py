from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.separation.dummy_multi_stem_separator import DummyMultiStemSeparator


def test_m80_measure_content_debug():

    context = AnalysisPipeline(
        separator=DummyMultiStemSeparator()
    ).analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    assert context.reconstructed_measures == ()
    assert context.analytical_score.measures == ()
