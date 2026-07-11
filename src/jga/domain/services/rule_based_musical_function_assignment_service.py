from datetime import datetime
from uuid import uuid4

from jga.domain.musical_function import MusicalFunction
from jga.domain.services.musical_function_assignment_service import (
    MusicalFunctionAssignmentService,
)
from jga.domain.sound_source import SoundSource


class RuleBasedMusicalFunctionAssignmentService(
    MusicalFunctionAssignmentService,
):

    def assign(
        self,
        sources: tuple[SoundSource, ...],
    ) -> tuple[MusicalFunction, ...]:

        functions: list[MusicalFunction] = []

        for source in sources:

            name = source.name.lower()

            if name == "bass":
                function_name = "Walking Bass"
                metric = True

            elif name == "drums":
                function_name = "Time Keeping"
                metric = True

            elif name == "piano":
                function_name = "Comping"
                metric = True

            elif name == "voice":
                function_name = "Melody"
                metric = False

            else:
                function_name = "Unknown"
                metric = False

            functions.append(
                MusicalFunction(
                    id=uuid4(),
                    name=function_name,
                    description=None,
                    is_metric=metric,
                    created_at=datetime.now(),
                )
            )

        return tuple(functions)