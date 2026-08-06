from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_pipeline_has_validation_dataset_runner():
    pipeline = AnalysisPipeline()

    assert pipeline.validation_dataset_runner is not None
