"""Deterministic scientific Comparator for JGA-COMPARATOR-001."""

from collections.abc import Callable
from uuid import uuid4

from jga.comparator.errors import (
    BindingFailure,
    ComparatorBindingError,
    SchemaCompatibilityError,
    SchemaCompatibilityFailure,
)
from jga.comparator.models import (
    ComparisonEvidenceState,
    ComparisonProvenance,
    ComparisonResult,
    InstrumentationComparisonEvidence,
    SectionComparisonEvidence,
    SectionCorrespondenceState,
    SectionsComparisonEvidence,
    TempoComparisonEvidence,
    TimeSignatureComparisonEvidence,
)
from jga.ground_truth.models import GroundTruth
from jga.interfaces.validation import (
    AnalysisOutputState,
    ImmutableAnalysisRepresentation,
)
from jga.validation_catalog.models import ValidationItem


class ScientificComparator:
    """Compares approved immutable inputs without interpretation or repair."""

    PROTOCOL_ID = "JGA-COMPARATOR-001"
    SCHEMA_VERSION = "1"
    ACCEPTED_ANALYSIS_SCHEMAS = ("1",)
    ACCEPTED_GROUND_TRUTH_SCHEMAS = ("1",)
    ACCEPTED_VALIDATION_ITEM_SCHEMAS = ("1",)

    def __init__(
        self,
        identity_factory: Callable[[], str] | None = None,
    ) -> None:
        self._identity_factory = identity_factory or (lambda: str(uuid4()))

    def compare(
        self,
        validation_item: ValidationItem,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> ComparisonResult:
        execution_id = self._identity_factory()
        self._verify_schemas(execution_id, validation_item, analysis, ground_truth)
        self._verify_bindings(execution_id, validation_item, analysis, ground_truth)

        provenance = ComparisonProvenance(
            comparator_protocol_id=self.PROTOCOL_ID,
            comparator_schema_version=self.SCHEMA_VERSION,
            analysis_schema_revision=analysis.schema_revision,
            ground_truth_schema_version=ground_truth.provenance.schema_version,
            validation_item_schema_version=validation_item.provenance.schema_version,
            validation_item_id=validation_item.validation_item_id,
            ground_truth_id=ground_truth.ground_truth_id,
            analysis_execution_id=analysis.analysis_execution_id,
            analysis_content_fingerprint=analysis.content_fingerprint,
        )

        return ComparisonResult(
            comparison_result_id=self._identity_factory(),
            comparison_execution_id=execution_id,
            provenance=provenance,
            tempo=self._compare_tempo(analysis, ground_truth),
            time_signature=self._compare_time_signature(analysis, ground_truth),
            sections=self._compare_sections(analysis, ground_truth),
            instrumentation=self._compare_instrumentation(analysis, ground_truth),
        )

    def _verify_schemas(
        self,
        execution_id: str,
        validation_item: ValidationItem,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> None:
        declarations = (
            (
                "Immutable Analysis Representation",
                self.ACCEPTED_ANALYSIS_SCHEMAS,
                analysis.schema_revision,
            ),
            (
                "Ground Truth",
                self.ACCEPTED_GROUND_TRUTH_SCHEMAS,
                ground_truth.provenance.schema_version,
            ),
            (
                "Validation Item",
                self.ACCEPTED_VALIDATION_ITEM_SCHEMAS,
                validation_item.provenance.schema_version,
            ),
        )
        failures = tuple(
            SchemaCompatibilityFailure(
                boundary=boundary,
                accepted_versions=accepted,
                observed_version=observed,
            )
            for boundary, accepted, observed in declarations
            if observed not in accepted
        )
        if failures:
            raise SchemaCompatibilityError(
                comparison_execution_id=execution_id,
                protocol_id=self.PROTOCOL_ID,
                schema_version=self.SCHEMA_VERSION,
                failures=failures,
            )

    def _verify_bindings(
        self,
        execution_id: str,
        validation_item: ValidationItem,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> None:
        declarations = (
            (
                "validation_item_id",
                validation_item.validation_item_id,
                ground_truth.validation_item_id,
            ),
            (
                "ground_truth_id",
                validation_item.ground_truth_id,
                ground_truth.ground_truth_id,
            ),
            (
                "audio_checksum",
                validation_item.mp3_recording.sha256,
                analysis.audio_checksum,
            ),
        )
        failures = tuple(
            BindingFailure(binding=name, expected=expected, observed=observed)
            for name, expected, observed in declarations
            if observed != expected
        )
        if failures:
            raise ComparatorBindingError(
                comparison_execution_id=execution_id,
                protocol_id=self.PROTOCOL_ID,
                schema_version=self.SCHEMA_VERSION,
                failures=failures,
            )

    def _compare_tempo(
        self,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> TempoComparisonEvidence:
        output = analysis.tempo
        if output.state is not AnalysisOutputState.PRESENT:
            return TempoComparisonEvidence(
                evidence_id=self._identity_factory(),
                state=ComparisonEvidenceState(output.state.value),
                expected=ground_truth.tempo,
                observed=None,
                signed_difference=None,
                absolute_difference=None,
                unit="beats_per_minute",
            )

        observed = output.value
        assert observed is not None
        if observed.beat_unit != ground_truth.tempo.beat_unit:
            return TempoComparisonEvidence(
                evidence_id=self._identity_factory(),
                state=ComparisonEvidenceState.INCOMPATIBLE,
                expected=ground_truth.tempo,
                observed=observed,
                signed_difference=None,
                absolute_difference=None,
                unit="beats_per_minute",
            )

        difference = observed.beats_per_minute - ground_truth.tempo.beats_per_minute
        return TempoComparisonEvidence(
            evidence_id=self._identity_factory(),
            state=ComparisonEvidenceState.PRESENT,
            expected=ground_truth.tempo,
            observed=observed,
            signed_difference=difference,
            absolute_difference=abs(difference),
            unit="beats_per_minute",
        )

    def _compare_time_signature(
        self,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> TimeSignatureComparisonEvidence:
        output = analysis.time_signature
        if output.state is not AnalysisOutputState.PRESENT:
            return TimeSignatureComparisonEvidence(
                evidence_id=self._identity_factory(),
                state=ComparisonEvidenceState(output.state.value),
                expected=ground_truth.time_signature,
                observed=None,
                exact_match=None,
            )

        observed = output.value
        assert observed is not None
        exact_match = (
            observed.beats == ground_truth.time_signature.beats
            and observed.beat_type == ground_truth.time_signature.beat_type
        )
        return TimeSignatureComparisonEvidence(
            evidence_id=self._identity_factory(),
            state=ComparisonEvidenceState.PRESENT,
            expected=ground_truth.time_signature,
            observed=observed,
            exact_match=exact_match,
        )

    def _compare_sections(
        self,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> SectionsComparisonEvidence:
        output = analysis.sections
        quantity_evidence_id = self._identity_factory()
        if output.state is not AnalysisOutputState.PRESENT:
            return SectionsComparisonEvidence(
                evidence_id=quantity_evidence_id,
                state=ComparisonEvidenceState(output.state.value),
                sections=(),
            )

        observed_sections = output.value
        assert observed_sections is not None
        evidence: list[SectionComparisonEvidence] = []
        expected_names = {section.name for section in ground_truth.sections}

        for expected in ground_truth.sections:
            observed = tuple(
                section
                for section in observed_sections
                if section.name == expected.name
            )
            if len(observed) == 1:
                match = observed[0]
                evidence.append(
                    SectionComparisonEvidence(
                        evidence_id=self._identity_factory(),
                        correspondence_state=SectionCorrespondenceState.MATCHED,
                        section_name=expected.name,
                        expected=expected,
                        observed=observed,
                        signed_start_difference=(
                            match.start_full_measure - expected.start_full_measure
                        ),
                        signed_length_difference=(
                            match.measure_count - expected.measure_count
                        ),
                    )
                )
            elif not observed:
                evidence.append(
                    SectionComparisonEvidence(
                        evidence_id=self._identity_factory(),
                        correspondence_state=(
                            SectionCorrespondenceState.MISSING_EXPECTED
                        ),
                        section_name=expected.name,
                        expected=expected,
                        observed=(),
                        signed_start_difference=None,
                        signed_length_difference=None,
                    )
                )
            else:
                evidence.append(
                    SectionComparisonEvidence(
                        evidence_id=self._identity_factory(),
                        correspondence_state=(
                            SectionCorrespondenceState.AMBIGUOUS_CORRESPONDENCE
                        ),
                        section_name=expected.name,
                        expected=expected,
                        observed=observed,
                        signed_start_difference=None,
                        signed_length_difference=None,
                    )
                )

        for observed in observed_sections:
            if observed.name not in expected_names:
                evidence.append(
                    SectionComparisonEvidence(
                        evidence_id=self._identity_factory(),
                        correspondence_state=(
                            SectionCorrespondenceState.UNEXPECTED_OBSERVED
                        ),
                        section_name=observed.name,
                        expected=None,
                        observed=(observed,),
                        signed_start_difference=None,
                        signed_length_difference=None,
                    )
                )

        return SectionsComparisonEvidence(
            evidence_id=quantity_evidence_id,
            state=ComparisonEvidenceState.PRESENT,
            sections=tuple(evidence),
        )

    def _compare_instrumentation(
        self,
        analysis: ImmutableAnalysisRepresentation,
        ground_truth: GroundTruth,
    ) -> InstrumentationComparisonEvidence:
        output = analysis.instrumentation
        expected = frozenset(
            instrument.canonical_category for instrument in ground_truth.instruments
        )
        expected_categories = tuple(sorted(expected))
        if output.state is not AnalysisOutputState.PRESENT:
            return InstrumentationComparisonEvidence(
                evidence_id=self._identity_factory(),
                state=ComparisonEvidenceState(output.state.value),
                expected_categories=expected_categories,
                observed_categories=None,
                matching_categories=None,
                missing_categories=None,
                unexpected_categories=None,
            )

        value = output.value
        assert value is not None
        observed = frozenset(value)
        return InstrumentationComparisonEvidence(
            evidence_id=self._identity_factory(),
            state=ComparisonEvidenceState.PRESENT,
            expected_categories=expected_categories,
            observed_categories=tuple(sorted(observed)),
            matching_categories=tuple(sorted(expected & observed)),
            missing_categories=tuple(sorted(expected - observed)),
            unexpected_categories=tuple(sorted(observed - expected)),
        )
