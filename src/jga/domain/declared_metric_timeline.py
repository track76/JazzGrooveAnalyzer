"""Immutable declared phase origin and checksum-bound numeric scope."""

from dataclasses import dataclass
from decimal import Decimal

from jga.domain.declared_metric_reference import MetricReferenceProvenance
from jga.interfaces.scientific_value_origin import ScientificValueOrigin


@dataclass(frozen=True, slots=True)
class DeclaredQuarterPhaseOrigin:
    """Externally authorized quarter-reference phase, never inferred."""

    seconds: Decimal
    provenance: MetricReferenceProvenance

    def __post_init__(self) -> None:
        if self.seconds < 0:
            raise ValueError("phase origin must be non-negative")

    @property
    def origin(self) -> ScientificValueOrigin:
        return ScientificValueOrigin.DECLARED


@dataclass(frozen=True, slots=True)
class DeclaredAnalysisScope:
    """Exact numeric interval and asset identity authorized for analysis."""

    start_seconds: Decimal
    end_seconds: Decimal
    asset_sha256: str
    provenance: MetricReferenceProvenance

    def __post_init__(self) -> None:
        if self.start_seconds < 0:
            raise ValueError("scope start must be non-negative")
        if self.end_seconds <= self.start_seconds:
            raise ValueError("scope end must be greater than scope start")
        if len(self.asset_sha256) != 64:
            raise ValueError("asset_sha256 must be a SHA-256 hexadecimal digest")
        try:
            int(self.asset_sha256, 16)
        except ValueError as error:
            raise ValueError(
                "asset_sha256 must be a SHA-256 hexadecimal digest"
            ) from error
        if self.asset_sha256 != self.provenance.source_sha256:
            raise ValueError("scope asset and provenance checksums must agree")

    @property
    def duration_seconds(self) -> Decimal:
        return self.end_seconds - self.start_seconds

    @property
    def origin(self) -> ScientificValueOrigin:
        return ScientificValueOrigin.DECLARED
