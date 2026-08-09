"""Immutable observational representations of externally produced Candidate Periods."""

from dataclasses import dataclass
from decimal import Decimal


def _require_text(value: str, field_name: str) -> None:
    if not value:
        raise ValueError(f"{field_name} must not be empty.")


def _require_non_negative(value: Decimal, field_name: str) -> None:
    if not value.is_finite() or value < 0:
        raise ValueError(f"{field_name} must be finite and non-negative.")


@dataclass(frozen=True, slots=True)
class CandidatePeriodOccurrence:
    """Two supporting observations whose temporal relation recurred."""

    start_observation_index: int
    end_observation_index: int
    start_seconds: Decimal
    end_seconds: Decimal

    def __post_init__(self) -> None:
        if self.start_observation_index < 0:
            raise ValueError("start_observation_index must be non-negative.")
        if self.end_observation_index <= self.start_observation_index:
            raise ValueError(
                "end_observation_index must follow start_observation_index."
            )
        _require_non_negative(self.start_seconds, "start_seconds")
        _require_non_negative(self.end_seconds, "end_seconds")
        if self.end_seconds <= self.start_seconds:
            raise ValueError("end_seconds must follow start_seconds.")


@dataclass(frozen=True, slots=True)
class CandidatePeriod:
    """A duration and its externally produced recurrence evidence."""

    duration_seconds: Decimal
    recurrence_evidence: tuple[CandidatePeriodOccurrence, ...]

    def __post_init__(self) -> None:
        if not self.duration_seconds.is_finite() or self.duration_seconds <= 0:
            raise ValueError("duration_seconds must be finite and positive.")
        if len(self.recurrence_evidence) < 2:
            raise ValueError(
                "A Candidate Period requires at least two recurrence occurrences."
            )


@dataclass(frozen=True, slots=True)
class CandidatePeriodObservationScope:
    """Declared observation population, source and temporal extent."""

    observation_population_id: str
    source_identity: str
    start_seconds: Decimal
    end_seconds: Decimal

    def __post_init__(self) -> None:
        _require_text(self.observation_population_id, "observation_population_id")
        _require_text(self.source_identity, "source_identity")
        _require_non_negative(self.start_seconds, "start_seconds")
        _require_non_negative(self.end_seconds, "end_seconds")
        if self.end_seconds < self.start_seconds:
            raise ValueError("end_seconds must not precede start_seconds.")


@dataclass(frozen=True, slots=True)
class CandidatePeriodProvenance:
    """Minimum runtime lineage of an externally produced population."""

    input_asset_path: str
    input_asset_sha256: str
    discovery_configuration: tuple[tuple[str, str], ...]
    source_revision: str | None = None

    def __post_init__(self) -> None:
        for field_name in (
            "input_asset_path",
            "input_asset_sha256",
        ):
            _require_text(getattr(self, field_name), field_name)
        if self.source_revision is not None:
            _require_text(self.source_revision, "source_revision")
        if any(
            not key or not value
            for key, value in self.discovery_configuration
        ):
            raise ValueError(
                "discovery_configuration keys and values must not be empty."
            )


@dataclass(frozen=True, slots=True)
class CandidatePeriodPopulation:
    """Complete immutable Candidate Period evidence for one declared scope."""

    observation_scope: CandidatePeriodObservationScope
    provenance: CandidatePeriodProvenance
    measurement_unit: str
    candidates: tuple[CandidatePeriod, ...]

    def __post_init__(self) -> None:
        _require_text(self.measurement_unit, "measurement_unit")
