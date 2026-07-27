from jga.representation.pipeline import RepresentationPipeline


def test_pipeline_has_metric_point_builder():

    pipeline = RepresentationPipeline()

    assert hasattr(pipeline, "_metric_point_builder")
