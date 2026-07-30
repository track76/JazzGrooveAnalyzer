from dataclasses import dataclass

from jga.domain.musical_function import MusicalFunction
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)


@dataclass(frozen=True, slots=True)
class MusicalFunctionAssignmentResult:
    """
    Result of musical function assignment.

    Preserves both:
    - assigned musical functions;
    - explicit source/function relationships.
    """

    musical_functions: tuple[MusicalFunction, ...]

    assignments: tuple[
        SourceMusicalFunctionAssignment,
        ...,
    ]
