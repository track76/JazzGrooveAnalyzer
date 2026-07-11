"""
Smoke tests.

These tests verify that the JGA package
can be imported correctly.
"""


def test_import_jga():

    import jga

    assert jga is not None


def test_import_pipeline():

    from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

    assert AnalysisPipeline is not None


def test_import_domain():

    from jga.core.eme import EME

    assert EME is not None