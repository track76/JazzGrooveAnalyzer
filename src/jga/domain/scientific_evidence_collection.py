from dataclasses import dataclass


from jga.domain.scientific_evidence import (
    ScientificEvidence,
)


@dataclass(
    frozen=True,
    slots=True,
)
class ScientificEvidenceCollection:
    """
    Collection of validated scientific evidence.
    """

    evidences: tuple[ScientificEvidence, ...]
