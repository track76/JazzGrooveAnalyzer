from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from pathlib import Path

import pytest

from jga.comparator import (
    ComparatorBindingError,
    ComparisonEvidenceState,
    SchemaCompatibilityError,
    ScientificComparator,
    SectionCorrespondenceState,
)
from jga.ground_truth.loaders import MusicXmlGroundTruthLoader
from jga.interfaces.validation import (
    AnalysisOutput,
    AnalysisOutputState,
    AnalysisSection,
    AnalysisTempo,
    AnalysisTimeSignature,
)
from jga.validation_catalog.loaders import RepositoryValidationCatalogLoader

from ._helpers import FakeImmutableAnalysis


ROOT = Path(".")
MUSICXML = Path(
    "recordings/validation/ground_truth/"
    "03 THE COST OF LIVING versione intro + 8 bar.musicxml"
)


def inputs(analysis: FakeImmutableAnalysis | None = None):
    item = RepositoryValidationCatalogLoader().load(ROOT).item("VAL-001")
    ground_truth = MusicXmlGroundTruthLoader().load(MUSICXML)
    return item, analysis or FakeImmutableAnalysis(), ground_truth


def test_tempo_preserves_signed_and_absolute_difference():
    result = ScientificComparator().compare(*inputs())

    assert result.tempo.state is ComparisonEvidenceState.PRESENT
    assert result.tempo.expected.beats_per_minute == Decimal("78")
    assert result.tempo.observed.beats_per_minute == Decimal("80")
    assert result.tempo.signed_difference == Decimal("2")
    assert result.tempo.absolute_difference == Decimal("2")
    assert result.tempo.unit == "beats_per_minute"


def test_tempo_with_different_beat_unit_is_incompatible():
    analysis = FakeImmutableAnalysis(
        tempo=AnalysisOutput(
            AnalysisOutputState.PRESENT,
            AnalysisTempo(Decimal("78"), "half"),
        )
    )

    evidence = ScientificComparator().compare(*inputs(analysis)).tempo

    assert evidence.state is ComparisonEvidenceState.INCOMPATIBLE
    assert evidence.observed.beat_unit == "half"
    assert evidence.signed_difference is None
    assert evidence.absolute_difference is None


def test_time_signature_preserves_exact_match_without_score():
    analysis = FakeImmutableAnalysis(
        time_signature=AnalysisOutput(
            AnalysisOutputState.PRESENT,
            AnalysisTimeSignature(3, 4),
        )
    )

    evidence = ScientificComparator().compare(*inputs(analysis)).time_signature

    assert evidence.state is ComparisonEvidenceState.PRESENT
    assert evidence.expected.beats == 4
    assert evidence.observed.beats == 3
    assert evidence.exact_match is False
    assert not hasattr(evidence, "score")


def test_sections_preserve_every_correspondence_state_without_inference():
    analysis = FakeImmutableAnalysis(
        sections=AnalysisOutput(
            AnalysisOutputState.PRESENT,
            (
                AnalysisSection("Intro", 1, 4),
                AnalysisSection("Intro", 2, 3),
                AnalysisSection("B", 5, 8),
            ),
        )
    )

    evidence = ScientificComparator().compare(*inputs(analysis)).sections
    by_state = {
        state: tuple(
            section
            for section in evidence.sections
            if section.correspondence_state is state
        )
        for state in SectionCorrespondenceState
    }

    assert len(by_state[SectionCorrespondenceState.AMBIGUOUS_CORRESPONDENCE]) == 1
    assert len(
        by_state[SectionCorrespondenceState.AMBIGUOUS_CORRESPONDENCE][0].observed
    ) == 2
    assert by_state[SectionCorrespondenceState.MISSING_EXPECTED][0].section_name == "A"
    assert by_state[SectionCorrespondenceState.UNEXPECTED_OBSERVED][0].section_name == "B"
    assert sum(len(section.observed) for section in evidence.sections) == 3


def test_matched_sections_preserve_signed_start_and_length_differences():
    analysis = FakeImmutableAnalysis(
        sections=AnalysisOutput(
            AnalysisOutputState.PRESENT,
            (
                AnalysisSection("Intro", 2, 3),
                AnalysisSection("A", 6, 10),
            ),
        )
    )

    sections = ScientificComparator().compare(*inputs(analysis)).sections.sections

    assert tuple(section.correspondence_state for section in sections) == (
        SectionCorrespondenceState.MATCHED,
        SectionCorrespondenceState.MATCHED,
    )
    assert sections[0].signed_start_difference == 1
    assert sections[0].signed_length_difference == -1
    assert sections[1].signed_start_difference == 1
    assert sections[1].signed_length_difference == 2


def test_instrumentation_is_compared_as_sets():
    analysis = FakeImmutableAnalysis(
        instrumentation=AnalysisOutput(
            AnalysisOutputState.PRESENT,
            ("Voice", "Piano", "Piano", "Guitar"),
        )
    )

    evidence = ScientificComparator().compare(*inputs(analysis)).instrumentation

    assert evidence.observed_categories == ("Guitar", "Piano", "Voice")
    assert evidence.matching_categories == ("Piano", "Voice")
    assert evidence.missing_categories == (
        "Double Bass",
        "Drum Set",
        "Saxophone",
    )
    assert evidence.unexpected_categories == ("Guitar",)


@pytest.mark.parametrize(
    "state",
    (
        AnalysisOutputState.EMPTY,
        AnalysisOutputState.NOT_PRODUCED,
        AnalysisOutputState.UNAVAILABLE,
        AnalysisOutputState.OUT_OF_SCOPE,
    ),
)
def test_non_present_availability_is_preserved_without_inference(state):
    analysis = FakeImmutableAnalysis(tempo=AnalysisOutput(state))

    evidence = ScientificComparator().compare(*inputs(analysis)).tempo

    assert evidence.state.value == state.value
    assert evidence.observed is None
    assert evidence.signed_difference is None
    assert evidence.absolute_difference is None


def test_mandatory_binding_failures_stop_before_comparison_evidence():
    item, analysis, ground_truth = inputs()
    invalid_item = replace(
        item,
        validation_item_id="VAL-OTHER",
        ground_truth_id="GT-OTHER",
    )
    invalid_analysis = FakeImmutableAnalysis(audio_checksum="wrong-checksum")

    with pytest.raises(ComparatorBindingError) as captured:
        ScientificComparator().compare(
            invalid_item,
            invalid_analysis,
            ground_truth,
        )

    error = captured.value
    assert error.protocol_id == "JGA-COMPARATOR-001"
    assert error.schema_version == "1"
    assert {failure.binding for failure in error.failures} == {
        "validation_item_id",
        "ground_truth_id",
        "audio_checksum",
    }
    assert not hasattr(error, "comparison_evidence")


def test_incompatible_schema_stops_before_comparison_evidence():
    item, _, ground_truth = inputs()
    analysis = FakeImmutableAnalysis(schema_revision="2")
    invalid_item = replace(
        item,
        provenance=replace(item.provenance, schema_version="2"),
    )
    invalid_ground_truth = replace(
        ground_truth,
        provenance=replace(ground_truth.provenance, schema_version="2"),
    )

    with pytest.raises(SchemaCompatibilityError) as captured:
        ScientificComparator().compare(
            invalid_item,
            analysis,
            invalid_ground_truth,
        )

    assert {failure.boundary for failure in captured.value.failures} == {
        "Immutable Analysis Representation",
        "Ground Truth",
        "Validation Item",
    }
    assert not hasattr(captured.value, "comparison_evidence")


def test_result_and_evidence_identities_are_unique_within_execution():
    result = ScientificComparator().compare(*inputs())
    evidence_ids = {
        result.tempo.evidence_id,
        result.time_signature.evidence_id,
        result.sections.evidence_id,
        result.instrumentation.evidence_id,
        *(section.evidence_id for section in result.sections.sections),
    }

    assert len(evidence_ids) == 6
    assert result.comparison_result_id not in evidence_ids
    assert result.comparison_execution_id not in evidence_ids
    assert result.comparison_result_id != result.comparison_execution_id


def test_execution_identity_is_distinct_from_scientific_content_equivalence():
    comparator = ScientificComparator()

    first = comparator.compare(*inputs())
    second = comparator.compare(*inputs())

    assert first.comparison_execution_id != second.comparison_execution_id
    assert first.comparison_result_id != second.comparison_result_id
    assert first.tempo.signed_difference == second.tempo.signed_difference
    assert first.time_signature.exact_match == second.time_signature.exact_match
    assert tuple(
        (
            section.correspondence_state,
            section.signed_start_difference,
            section.signed_length_difference,
        )
        for section in first.sections.sections
    ) == tuple(
        (
            section.correspondence_state,
            section.signed_start_difference,
            section.signed_length_difference,
        )
        for section in second.sections.sections
    )


def test_comparison_result_is_immutable_and_scope_minimal():
    result = ScientificComparator().compare(*inputs())

    with pytest.raises(FrozenInstanceError):
        result.comparison_result_id = "changed"

    with pytest.raises(FrozenInstanceError):
        result.tempo.signed_difference = Decimal("0")

    assert not hasattr(result, "pickup")
    assert not hasattr(result, "normalized_measure_count")
    assert not hasattr(result, "accuracy")
    assert not hasattr(result, "conclusion")
