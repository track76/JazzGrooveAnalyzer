"""Immutable scientific comparison evidence and result models."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from jga.ground_truth.models import (
    GroundTruthSection,
    GroundTruthTempo,
    GroundTruthTimeSignature,
)
from jga.interfaces.validation import (
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
)


class ComparisonEvidenceState(str, Enum):
    PRESENT = "PRESENT"
    EMPTY = "EMPTY"
    NOT_PRODUCED = "NOT_PRODUCED"
    UNAVAILABLE = "UNAVAILABLE"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    INCOMPATIBLE = "INCOMPATIBLE"


class SectionCorrespondenceState(str, Enum):
    MATCHED = "MATCHED"
    MISSING_EXPECTED = "MISSING_EXPECTED"
    AMBIGUOUS_CORRESPONDENCE = "AMBIGUOUS_CORRESPONDENCE"
    UNEXPECTED_OBSERVED = "UNEXPECTED_OBSERVED"


@dataclass(frozen=True, slots=True)
class ComparisonProvenance:
    comparator_protocol_id: str
    comparator_schema_version: str
    analysis_schema_revision: str
    ground_truth_schema_version: str
    validation_item_schema_version: str
    validation_item_id: str
    ground_truth_id: str
    analysis_execution_id: str
    analysis_content_fingerprint: str


@dataclass(frozen=True, slots=True)
class TempoComparisonEvidence:
    evidence_id: str
    state: ComparisonEvidenceState
    expected: GroundTruthTempo
    observed: AnalysisTempo | None
    signed_difference: Decimal | None
    absolute_difference: Decimal | None
    unit: str


@dataclass(frozen=True, slots=True)
class TimeSignatureComparisonEvidence:
    evidence_id: str
    state: ComparisonEvidenceState
    expected: GroundTruthTimeSignature
    observed: AnalysisTimeSignature | None
    exact_match: bool | None


@dataclass(frozen=True, slots=True)
class SectionComparisonEvidence:
    evidence_id: str
    correspondence_state: SectionCorrespondenceState
    section_name: str
    expected: GroundTruthSection | None
    observed: tuple[AnalysisSection, ...]
    signed_start_difference: int | None
    signed_length_difference: int | None


@dataclass(frozen=True, slots=True)
class SectionsComparisonEvidence:
    evidence_id: str
    state: ComparisonEvidenceState
    sections: tuple[SectionComparisonEvidence, ...]


@dataclass(frozen=True, slots=True)
class InstrumentationComparisonEvidence:
    evidence_id: str
    state: ComparisonEvidenceState
    expected_categories: tuple[str, ...]
    observed_categories: tuple[str, ...] | None
    matching_categories: tuple[str, ...] | None
    missing_categories: tuple[str, ...] | None
    unexpected_categories: tuple[str, ...] | None


@dataclass(frozen=True, slots=True)
class ComparisonResult:
    comparison_result_id: str
    comparison_execution_id: str
    provenance: ComparisonProvenance
    tempo: TempoComparisonEvidence
    time_signature: TimeSignatureComparisonEvidence
    sections: SectionsComparisonEvidence
    instrumentation: InstrumentationComparisonEvidence
