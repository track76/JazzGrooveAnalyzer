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
from uuid import uuid4

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

            for candidate in sequence.pulse_candidates:

                result.append(
                    PulseCandidate(
                        id=uuid4(),
                        sound_source_id=sound_source_id,
                        timestamp=float(
                            candidate.time
                        ),
                        strength=candidate.strength,
                        confidence=float(
                            candidate.confidence
                        ),
                        created_at=datetime.now(),
                    )
                )

        return tuple(result)
