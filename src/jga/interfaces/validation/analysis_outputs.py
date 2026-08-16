"""Typed validation-facing outputs of immutable analysis."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Generic, TypeVar

from jga.interfaces.scientific_value_origin import ScientificValueOrigin


class AnalysisOutputState(str, Enum):
    """Canonical availability state of a validation-facing output."""

    PRESENT = "PRESENT"
    EMPTY = "EMPTY"
    NOT_PRODUCED = "NOT_PRODUCED"
    UNAVAILABLE = "UNAVAILABLE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"


@dataclass(frozen=True, slots=True)
class AnalysisTempo:
    beats_per_minute: Decimal
    beat_unit: str


@dataclass(frozen=True, slots=True)
class AnalysisOutputProvenance:
    """Authority and scope for one non-observational scientific value."""

    source_id: str
    source_kind: str
    source_sha256: str
    temporal_scope: str


@dataclass(frozen=True, slots=True)
class AnalysisTimeSignature:
    beats: int
    beat_type: int


@dataclass(frozen=True, slots=True)
class AnalysisSection:
    name: str
    start_full_measure: int
    measure_count: int


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class AnalysisOutput(Generic[T]):
    """One typed output with explicit, non-inferred availability."""

    state: AnalysisOutputState
    value: T | None = None
    origin: ScientificValueOrigin | None = None
    provenance: AnalysisOutputProvenance | None = None

    def __post_init__(self) -> None:
        if self.state is AnalysisOutputState.PRESENT and self.value is None:
            raise ValueError("PRESENT analysis output requires a value.")
        if self.state is not AnalysisOutputState.PRESENT and self.value is not None:
            raise ValueError("Non-PRESENT analysis output cannot contain a value.")
        if self.state is not AnalysisOutputState.PRESENT and (
            self.origin is not None or self.provenance is not None
        ):
            raise ValueError(
                "Non-PRESENT analysis output cannot contain origin or provenance."
            )
        if (self.origin is None) != (self.provenance is None):
            raise ValueError("origin and provenance must be supplied together.")
