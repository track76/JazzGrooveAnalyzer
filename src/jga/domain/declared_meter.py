"""Immutable externally declared meter context."""

from dataclasses import dataclass

from jga.domain.declared_metric_reference import MetricReferenceProvenance
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


@dataclass(frozen=True, slots=True)
class DeclaredMeter:
    """Musical meter supplied by authority, never inferred from audio."""

    numerator: int
    denominator: int
    provenance: MetricReferenceProvenance

    def __post_init__(self) -> None:
        if self.numerator <= 0:
            raise ValueError("numerator must be positive")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")

    @property
    def origin(self) -> ScientificValueOrigin:
        return ScientificValueOrigin.DECLARED

    def __str__(self) -> str:
        return f"{self.numerator}/{self.denominator}"
