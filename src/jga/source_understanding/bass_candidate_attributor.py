from typing import Protocol

from jga.domain.pulse_candidate import PulseCandidate
from jga.source_understanding.bass_candidate_attribution import (
    BassCandidateAttribution,
    CandidateInputRepresentation,
)


class BassCandidateAttributor(Protocol):
    """Classify candidates without redefining their technical source identity."""

    def attribute(
        self,
        candidate: PulseCandidate,
        input_representation: CandidateInputRepresentation,
    ) -> BassCandidateAttribution:
        ...
