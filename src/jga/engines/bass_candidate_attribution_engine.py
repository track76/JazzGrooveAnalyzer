from collections.abc import Iterable

from jga.domain.pulse_candidate import PulseCandidate
from jga.source_understanding.bass_candidate_attribution import (
    BassCandidateAttribution,
    CandidateInputRepresentation,
)
from jga.source_understanding.bass_candidate_attributor import (
    BassCandidateAttributor,
)
from jga.source_understanding.unknown_bass_candidate_attributor import (
    UnknownBassCandidateAttributor,
)


class BassCandidateAttributionEngine:
    """Attach attribution decisions to candidates without changing them."""

    def __init__(
        self,
        attributor: BassCandidateAttributor | None = None,
    ) -> None:
        self._attributor = attributor or UnknownBassCandidateAttributor()

    def attribute(
        self,
        candidates: Iterable[PulseCandidate],
        input_representation: CandidateInputRepresentation,
    ) -> tuple[BassCandidateAttribution, ...]:
        return tuple(
            self._attributor.attribute(candidate, input_representation)
            for candidate in candidates
        )
