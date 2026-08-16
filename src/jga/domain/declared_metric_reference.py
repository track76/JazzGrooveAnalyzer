"""Immutable externally declared metric-reference context."""

from dataclasses import dataclass
from decimal import Decimal

from jga.interfaces.scientific_value_origin import ScientificValueOrigin


@dataclass(frozen=True, slots=True)
class MetricReferenceProvenance:
    """Stable identity of the authority supplying a declared reference."""

    source_id: str
    source_kind: str
    source_sha256: str
    temporal_scope: str

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must not be empty")
        if not self.source_kind.strip():
            raise ValueError("source_kind must not be empty")
        if len(self.source_sha256) != 64:
            raise ValueError("source_sha256 must be a SHA-256 hexadecimal digest")
        try:
            int(self.source_sha256, 16)
        except ValueError as error:
            raise ValueError(
                "source_sha256 must be a SHA-256 hexadecimal digest"
            ) from error
        if not self.temporal_scope.strip():
            raise ValueError("temporal_scope must not be empty")


@dataclass(frozen=True, slots=True)
class DeclaredMetricReference:
    """Musical reference supplied by authority, never inferred from audio."""

    beats_per_minute: Decimal
    beat_unit: str
    provenance: MetricReferenceProvenance

    def __post_init__(self) -> None:
        if self.beats_per_minute <= 0:
            raise ValueError("beats_per_minute must be positive")
        if not self.beat_unit.strip():
            raise ValueError("beat_unit must not be empty")

    @property
    def origin(self) -> ScientificValueOrigin:
        return ScientificValueOrigin.DECLARED

    @property
    def period_seconds(self) -> Decimal:
        return Decimal("60") / self.beats_per_minute
