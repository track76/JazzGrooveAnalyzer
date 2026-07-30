from jga.domain.ensemble_analysis_result import (
    EnsembleAnalysisResult,
)
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


def test_ensemble_analysis_result_contains_assignments():

    result = EnsembleAnalysisResult(
        sound_sources=(),
        musical_functions=(),
        source_function_assignments=(),
        metric_contributors=(),
    )

    assert isinstance(
        result.source_function_assignments,
        tuple,
    )
