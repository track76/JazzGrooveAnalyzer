from jga.runtime.analysis_context import AnalysisContext
from jga.representation.representation_result import (
    RepresentationResult,
)


def test_analysis_context_accepts_representation_result():

    context = AnalysisContext(audio=None)

    representation = RepresentationResult()

    context.representation_result = representation

    assert context.representation_result is representation
