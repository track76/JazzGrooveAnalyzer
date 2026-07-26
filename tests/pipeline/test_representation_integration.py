from jga.pipeline.default_analysis_pipeline import AnalysisPipeline


def test_analysis_pipeline_exposes_representation_pipeline():

    pipeline = AnalysisPipeline()

    assert hasattr(
        pipeline,
        "representation_pipeline",
    )
