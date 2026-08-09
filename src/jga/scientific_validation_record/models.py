"""Immutable Scientific Validation Record model."""

from dataclasses import dataclass

from jga.comparator.models import ComparisonProvenance, ComparisonResult


class ValidationRecordBindingError(Exception):
    """Raised when immutable analysis and comparison identities do not bind."""


@dataclass(frozen=True, slots=True)
class ScientificValidationRecord:
    """Permanent evidence for one completed scientific validation execution."""

    record_id: str
    record_fingerprint: str
    validation_item_id: str
    ground_truth_id: str
    analysis_execution_id: str
    analysis_content_fingerprint: str
    comparator_execution_id: str
    comparison_result_id: str
    comparator_protocol_id: str
    comparator_schema_version: str
    input_provenance: ComparisonProvenance
    comparison_result: ComparisonResult
    limitations: tuple[str, ...]
