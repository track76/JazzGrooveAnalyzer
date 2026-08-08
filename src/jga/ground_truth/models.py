"""Immutable scientific Ground Truth representations."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class AuthoritativeSourceProvenance:
    """Identity and integrity of an authoritative symbolic source."""

    repository_path: str
    sha256: str
    repository_revision: str | None = None


@dataclass(frozen=True, slots=True)
class GroundTruthProvenance:
    """Schema, normalization and source provenance for Ground Truth."""

    schema_version: str
    normalization_version: str
    source: AuthoritativeSourceProvenance


@dataclass(frozen=True, slots=True)
class GroundTruthTimeSignature:
    """Observable notated time signature."""

    beats: int
    beat_type: int


@dataclass(frozen=True, slots=True)
class GroundTruthTempo:
    """Observable notated metronome indication."""

    beats_per_minute: Decimal
    beat_unit: str


@dataclass(frozen=True, slots=True)
class GroundTruthMeasure:
    """Traceable mapping from source measure to normalized metric position."""

    source_measure_id: str
    normalized_full_measure: int | None
    is_pickup: bool


@dataclass(frozen=True, slots=True)
class GroundTruthSection:
    """Section boundary expressed in normalized full measures."""

    name: str
    start_full_measure: int
    measure_count: int


@dataclass(frozen=True, slots=True)
class GroundTruthInstrument:
    """Original MusicXML designation and canonical VAL-001 category."""

    source_part_id: str
    source_part_name: str
    source_instrument_name: str
    canonical_category: str


@dataclass(frozen=True, slots=True)
class GroundTruth:
    """Minimum immutable Ground Truth reference for later validation."""

    ground_truth_id: str
    validation_dataset_id: str
    provenance: GroundTruthProvenance
    time_signature: GroundTruthTimeSignature
    tempo: GroundTruthTempo
    measures: tuple[GroundTruthMeasure, ...]
    sections: tuple[GroundTruthSection, ...]
    instruments: tuple[GroundTruthInstrument, ...]
