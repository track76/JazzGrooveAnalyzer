from jga.domain.pulse_candidate import PulseCandidate
from jga.source_understanding.bass_candidate_attribution import (
    BassAttributionDecision,
    BassCandidateAttribution,
    CandidateInputRepresentation,
)


class UnknownBassCandidateAttributor:
    """Fail-closed default until a separately authorized recognizer exists."""

    def attribute(
        self,
        candidate: PulseCandidate,
        input_representation: CandidateInputRepresentation,
    ) -> BassCandidateAttribution:
        return BassCandidateAttribution(
            candidate_id=candidate.id,
            source_id=candidate.sound_source_id,
            timestamp=candidate.timestamp,
            decision=BassAttributionDecision.UNKNOWN,
            input_representation=input_representation,
            observation_index=candidate.observation_index,
            observation_provenance_id=candidate.observation_provenance_id,
        )
