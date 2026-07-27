from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class ScientificEvidence:
    """
    One scientific measurement together with its
    diagnostic interpretation.
    """

    name: str

    value: float

    reference: float

    delta: float

    tolerance: float

    compatible: bool

