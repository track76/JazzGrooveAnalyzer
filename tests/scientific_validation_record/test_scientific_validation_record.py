from dataclasses import FrozenInstanceError
from itertools import count
from pathlib import Path

import pytest

from jga.comparator import ComparisonEvidenceState, ScientificComparator
from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
from jga.scientific_validation_record import (
    ScientificValidationRecordMaterializer,
    ValidationRecordBindingError,
)
from jga.validation_catalog.loaders import RepositoryValidationCatalogLoader
from tests.comparator._helpers import FakeImmutableAnalysis


def identity_factory():
    identities = count(1)
    return lambda: f"IDENTITY-{next(identities)}"


def comparison(analysis=None):
    analysis = analysis or FakeImmutableAnalysis()
    result = ScientificComparator(identity_factory()).compare(
        RepositoryValidationCatalogLoader().load(Path(".")).item("VAL-001"),
        analysis,
        MusicXmlGroundTruthLoader().load(
            Path(
                "recordings/validation/ground_truth/"
                "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
            )
        ),
    )
    return analysis, result


def test_record_preserves_all_input_identities_and_provenance():
    analysis, result = comparison()
    record = ScientificValidationRecordMaterializer().materialize(result, analysis)

    assert record.validation_item_id == "VAL-001"
    assert record.ground_truth_id == "GT-VAL-001-v1"
    assert record.analysis_execution_id == analysis.analysis_execution_id
    assert record.analysis_content_fingerprint == analysis.content_fingerprint
    assert record.comparator_execution_id == result.comparison_execution_id
    assert record.comparison_result_id == result.comparison_result_id
    assert record.comparator_protocol_id == "JGA-COMPARATOR-001"
    assert record.comparator_schema_version == "1"
    assert record.input_provenance is result.provenance
    assert record.comparison_result is result
    assert record.limitations == analysis.limitations


def test_record_preserves_evidence_and_availability_states_unchanged():
    analysis, result = comparison()
    record = ScientificValidationRecordMaterializer().materialize(result, analysis)

    assert record.comparison_result.tempo is result.tempo
    assert record.comparison_result.time_signature is result.time_signature
    assert record.comparison_result.sections is result.sections
    assert record.comparison_result.instrumentation is result.instrumentation
    assert record.comparison_result.tempo.state is ComparisonEvidenceState.PRESENT


def test_record_identity_and_fingerprint_are_deterministic():
    analysis, result = comparison()
    materializer = ScientificValidationRecordMaterializer()

    first = materializer.materialize(result, analysis)
    second = materializer.materialize(result, analysis)

    assert first == second
    assert first.record_id == second.record_id
    assert first.record_fingerprint == second.record_fingerprint
    assert first.record_id == f"JGA-SVR-{first.record_fingerprint}"


def test_record_and_nested_evidence_are_deeply_immutable():
    analysis, result = comparison()
    record = ScientificValidationRecordMaterializer().materialize(result, analysis)

    with pytest.raises(FrozenInstanceError):
        record.record_id = "changed"
    with pytest.raises(FrozenInstanceError):
        record.comparison_result.tempo.state = ComparisonEvidenceState.UNAVAILABLE


def test_materializer_rejects_analysis_identity_or_content_mismatch():
    analysis, result = comparison()

    class WrongExecutionAnalysis(FakeImmutableAnalysis):
        @property
        def analysis_execution_id(self) -> str:
            return "OTHER-EXECUTION"

    wrong_execution = WrongExecutionAnalysis()

    with pytest.raises(ValidationRecordBindingError):
        ScientificValidationRecordMaterializer().materialize(
            result,
            wrong_execution,
        )

    assert wrong_execution.content_fingerprint == analysis.content_fingerprint

    class WrongContentAnalysis(FakeImmutableAnalysis):
        @property
        def content_fingerprint(self) -> str:
            return "OTHER-CONTENT"

    with pytest.raises(ValidationRecordBindingError):
        ScientificValidationRecordMaterializer().materialize(
            result,
            WrongContentAnalysis(),
        )
