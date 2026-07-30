from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)


def test_assignment_result_contains_functions_and_assignments():

    result = MusicalFunctionAssignmentResult(
        musical_functions=(),
        assignments=(),
    )

    assert result.musical_functions == ()
    assert result.assignments == ()
