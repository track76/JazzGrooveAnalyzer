"""Comparator Result to Scientific Validation Record materialization."""

from dataclasses import fields, is_dataclass
from decimal import Decimal
from enum import Enum
from hashlib import sha256
import json

from jga.comparator.models import ComparisonResult
from jga.interfaces.validation import ImmutableAnalysisRepresentation
from jga.scientific_validation_record.models import (
    ScientificValidationRecord,
    ValidationRecordBindingError,
)


class ScientificValidationRecordMaterializer:
    """Preserves immutable comparison evidence without interpretation."""

    RECORD_ID_PREFIX = "JGA-SVR-"

    def materialize(
        self,
        comparison_result: ComparisonResult,
        analysis: ImmutableAnalysisRepresentation,
    ) -> ScientificValidationRecord:
        provenance = comparison_result.provenance
        if provenance.analysis_execution_id != analysis.analysis_execution_id:
            raise ValidationRecordBindingError(
                "Analysis execution identity does not bind to Comparator provenance."
            )
        if provenance.analysis_content_fingerprint != analysis.content_fingerprint:
            raise ValidationRecordBindingError(
                "Analysis content fingerprint does not bind to Comparator provenance."
            )

        payload = {
            "analysis_content_fingerprint": analysis.content_fingerprint,
            "analysis_execution_id": analysis.analysis_execution_id,
            "comparator_execution_id": comparison_result.comparison_execution_id,
            "comparison_result": self._canonical_value(comparison_result),
            "limitations": analysis.limitations,
        }
        fingerprint = sha256(
            json.dumps(
                payload,
                ensure_ascii=True,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()

        return ScientificValidationRecord(
            record_id=f"{self.RECORD_ID_PREFIX}{fingerprint}",
            record_fingerprint=fingerprint,
            validation_item_id=provenance.validation_item_id,
            ground_truth_id=provenance.ground_truth_id,
            analysis_execution_id=analysis.analysis_execution_id,
            analysis_content_fingerprint=analysis.content_fingerprint,
            comparator_execution_id=comparison_result.comparison_execution_id,
            comparison_result_id=comparison_result.comparison_result_id,
            comparator_protocol_id=provenance.comparator_protocol_id,
            comparator_schema_version=provenance.comparator_schema_version,
            input_provenance=provenance,
            comparison_result=comparison_result,
            limitations=tuple(analysis.limitations),
        )

    @classmethod
    def _canonical_value(cls, value: object) -> object:
        if is_dataclass(value):
            return {
                field.name: cls._canonical_value(getattr(value, field.name))
                for field in fields(value)
            }
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, Decimal):
            return str(value)
        if isinstance(value, tuple):
            return [cls._canonical_value(item) for item in value]
        if isinstance(value, frozenset):
            return sorted(cls._canonical_value(item) for item in value)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        raise TypeError(f"Unsupported scientific record value: {type(value).__name__}")
