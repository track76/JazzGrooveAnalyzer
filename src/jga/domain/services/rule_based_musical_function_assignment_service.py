from datetime import datetime
from uuid import uuid4

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
    ) -> tuple[SourceMusicalFunctionAssignment, ...]:

        assignments: list[SourceMusicalFunctionAssignment] = []

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

            assignments.append(
                SourceMusicalFunctionAssignment(
                    id=uuid4(),
                    sound_source_id=source.id,
                    musical_function_id=uuid4(),
                    confidence=0.8,
                    rationale=(
                        f"Assigned {function_name} "
                        f"from source family {family}"
                    ),
                    created_at=datetime.now(),
                )
            )

        return tuple(assignments)
