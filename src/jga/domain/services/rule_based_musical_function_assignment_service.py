from datetime import datetime
from uuid import uuid4

from jga.domain.musical_function import MusicalFunction
from jga.domain.musical_function_assignment_result import (
    MusicalFunctionAssignmentResult,
)
from jga.domain.services.musical_function_assignment_service import (
    MusicalFunctionAssignmentService,
)
from jga.domain.source_musical_function_assignment import (
    SourceMusicalFunctionAssignment,
)
from jga.domain.sound_source import SoundSource


class RuleBasedMusicalFunctionAssignmentService(
    MusicalFunctionAssignmentService,
):

    def assign(
        self,
        sources: tuple[SoundSource, ...],
    ) -> MusicalFunctionAssignmentResult:

        functions: list[MusicalFunction] = []

        assignments: list[
            SourceMusicalFunctionAssignment
        ] = []

        for source in sources:

            family = source.family.lower()

            if family == "bass":
                function_name = "Walking Bass"
                metric = True

            elif family == "percussion":
                function_name = "Time Keeping"
                metric = True

            elif family == "chordal":
                function_name = "Harmonic Support"
                metric = False

            elif family == "voice":
                function_name = "Melody"
                metric = False

            elif family == "wind":
                function_name = "Melody"
                metric = False

            else:
                function_name = "Unknown"
                metric = False

            function = MusicalFunction(
                id=uuid4(),
                name=function_name,
                description=None,
                is_metric=metric,
                created_at=datetime.now(),
            )

            functions.append(function)

            assignments.append(
                SourceMusicalFunctionAssignment(
                    id=uuid4(),
                    sound_source_id=source.id,
                    musical_function_id=function.id,
                    confidence=0.8,
                    rationale=(
                        f"Assigned {function_name} "
                        f"from source family {family}"
                    ),
                    created_at=datetime.now(),
                )
            )

        return MusicalFunctionAssignmentResult(
            musical_functions=tuple(functions),
            assignments=tuple(assignments),
        )
