"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_pulse_candidate_adapter.py

Description:
    Converts observable core PulseCandidates into
    domain PulseCandidates.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
=========================================================
"""

from datetime import datetime
from uuid import NAMESPACE_URL, uuid5

from jga.domain.pulse_candidate import (
    PulseCandidate,
)


class DomainPulseCandidateAdapter:
    """
    Converts core temporal observations into
    domain reconstruction candidates.
    """

    def convert(
        self,
        source_pulse_sequences,
        observation_scope_identity: str = "unspecified-observation-scope",
    ) -> tuple[PulseCandidate, ...]:

        result = []

        for sequence in source_pulse_sequences:

            if sequence.source.source_id is None:
                raise ValueError(
                    "MetricSource requires source_id."
                )

            sound_source_id = (
                sequence.source.source_id
            )

            for observation_index, candidate in enumerate(sequence.pulse_candidates):

                identity = ":".join(
                    (
                        "domain-pulse-candidate/v2",
                        observation_scope_identity,
                        str(sound_source_id),
                        str(observation_index),
                        candidate.time.hex(),
                        candidate.strength.hex(),
                        candidate.confidence.hex(),
                    )
                )

                result.append(
                    PulseCandidate(
                        id=uuid5(NAMESPACE_URL, identity),
                        sound_source_id=sound_source_id,
                        timestamp=float(
                            candidate.time
                        ),
                        strength=candidate.strength,
                        confidence=float(
                            candidate.confidence
                        ),
                        created_at=datetime.now(),
                        observation_index=observation_index,
                        observation_provenance_id=observation_scope_identity,
                    )
                )

        return tuple(result)
