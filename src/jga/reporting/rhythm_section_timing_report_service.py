"""Thin application orchestration for an AD-040 scientific JSON report."""

from __future__ import annotations

from hashlib import sha256
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import sys
from uuid import NAMESPACE_URL, uuid5

import librosa
import numpy

from jga.engines.pulse_candidate_builder import PulseCandidateBuilder
from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)
from jga.representation.builders.rhythm_section_timing_profile_builder import (
    RhythmSectionTimingProfileBuilder,
)
from jga.representation.rhythm_section_timing_profile import (
    AnalyticalRoleAssignment,
)
from jga.reporting.rhythm_section_timing_report import (
    AuthorizedSourceInput,
    RhythmSectionTimingReport,
    RhythmSectionTimingReportError,
)


SCHEMA_ID = "JGA_RHYTHM_SECTION_TIMING_REPORT_V1"
SCHEMA_VERSION = 1
ROLE_RULE = "caller-authorized-analytical-role/v1"
FINGERPRINT_RULE = "sha256-canonical-json-scientific-content/v1"
FRAME_COORDINATE_RULE = "verified-timestamp-frame-roundtrip/v1"
FIREWALL = (
    "beat_identity",
    "musical_correspondence",
    "tempo",
    "bpm",
    "meter",
    "downbeat",
    "swing",
    "groove",
    "rushing",
    "dragging",
    "intention",
    "human_microtiming",
    "physical_onset_ground_truth",
    "calibrated_timing_correction",
    "ACQUISITION_CLOCK_SYNCHRONY_NOT_ESTABLISHED",
)
CALIBRATION_APPLICABILITY_VALUES = {
    "APPLICABLE",
    "NOT_APPLICABLE",
    "UNESTABLISHED",
}


class RhythmSectionTimingReportService:
    """Compose unchanged JGA analysis, AD-038, AD-040, and JSON export."""

    def __init__(self, pipeline_factory=AnalysisPipeline) -> None:
        self._pipeline_factory = pipeline_factory
        self._localization_builder = DrumRelativeEMELocalizationBuilder()
        self._profile_builder = RhythmSectionTimingProfileBuilder()

    def build(
        self,
        sources: tuple[AuthorizedSourceInput, ...],
        *,
        execution_id: str,
        provenance_id: str,
        role_authority_id: str,
        role_authority_fingerprint: str,
        calibration_applicability: str,
        calibration_authority_id: str,
        calibration_authority_fingerprint: str,
        jga_revision: str,
    ) -> RhythmSectionTimingReport:
        self._validate_invocation(
            sources,
            execution_id,
            provenance_id,
            role_authority_id,
            role_authority_fingerprint,
            calibration_authority_id,
            calibration_authority_fingerprint,
            jga_revision,
        )
        if calibration_applicability not in CALIBRATION_APPLICABILITY_VALUES:
            raise RhythmSectionTimingReportError(
                "UNSUPPORTED_CALIBRATION_APPLICABILITY:"
                f"{calibration_applicability}"
            )
        ordered_sources = tuple(
            sorted(sources, key=lambda item: (item.role, item.label, str(item.path)))
        )
        analyses = []
        authorities = []
        assignments = []
        all_events = []
        all_candidates = []

        for source in ordered_sources:
            authority = self._source_authority(source)
            try:
                context = self._pipeline_factory().analyze(str(authority["path_used"]))
            except Exception as exc:
                raise RhythmSectionTimingReportError(
                    f"SOURCE_ANALYSIS_FAILURE:{source.label}:{type(exc).__name__}:{exc}"
                ) from exc
            events = tuple(context.elementary_metric_events)
            if not events:
                raise RhythmSectionTimingReportError(
                    f"EMPTY_EME_POPULATION:{source.label}"
                )
            source_ids = {event.sound_source_id for event in events}
            if None in source_ids or len(source_ids) != 1:
                raise RhythmSectionTimingReportError(
                    f"AMBIGUOUS_EME_SOURCE_IDENTITY:{source.label}"
                )
            asset_ids = {event.source_asset_sha256 for event in events}
            if asset_ids != {authority["sha256"]}:
                raise RhythmSectionTimingReportError(
                    f"EME_SOURCE_AUTHORITY_MISMATCH:{source.label}"
                )
            temporal_scopes = {event.temporal_scope for event in events}
            if len(temporal_scopes) != 1:
                raise RhythmSectionTimingReportError(
                    f"AMBIGUOUS_EME_TEMPORAL_SCOPE:{source.label}"
                )
            source_id = next(iter(source_ids))
            scope = next(iter(temporal_scopes))
            assignment_id = uuid5(
                NAMESPACE_URL,
                ":".join(
                    (
                        ROLE_RULE,
                        execution_id,
                        role_authority_id,
                        role_authority_fingerprint,
                        source.role,
                        source.label,
                        authority["sha256"],
                        str(source_id),
                    )
                ),
            )
            assignments.append(
                AnalyticalRoleAssignment(
                    assignment_id=assignment_id,
                    source_id=source_id,
                    asset_id=authority["sha256"],
                    temporal_scope=scope,
                    temporal_origin_seconds=0.0,
                    role=source.role,
                    assignment_rule=ROLE_RULE,
                    execution_id=execution_id,
                    scientific_authority_id=role_authority_id,
                    scientific_authority_fingerprint=role_authority_fingerprint,
                )
            )
            observation_records = self._observation_records(context, source.label)
            authority["source_identity"] = str(source_id)
            authority["technical_audio"] = {
                "format": context.audio.format,
                "sample_rate_hz": context.audio.sample_rate,
                "channel_count": context.audio.channels,
                "duration_seconds": context.audio.duration,
                "frame_count": round(context.audio.duration * context.audio.sample_rate),
            }
            authority["observation_count"] = len(observation_records)
            authority["eme_count"] = len(events)
            authorities.append(authority)
            analyses.append((source, context, events, observation_records))
            all_events.extend(events)
            all_candidates.extend(context.domain_pulse_candidates)

        scopes = {item.temporal_scope for item in assignments}
        if len(scopes) != 1:
            raise RhythmSectionTimingReportError("INCONSISTENT_SOURCE_TEMPORAL_SCOPE")
        reference_events = tuple(
            event
            for (source, _, events, _) in analyses
            if source.role == "TEMPORAL_REFERENCE"
            for event in events
        )
        target_events = tuple(
            event
            for (source, _, events, _) in analyses
            if source.role == "ACCOMPANIMENT"
            for event in events
        )
        if not reference_events:
            raise RhythmSectionTimingReportError("EMPTY_TEMPORAL_REFERENCE_EME_POPULATION")
        if not target_events:
            raise RhythmSectionTimingReportError("EMPTY_ACCOMPANIMENT_EME_POPULATION")

        try:
            localizations = self._localization_builder.build(
                target_events,
                reference_events,
                all_candidates,
                temporal_origin_seconds=0.0,
                analysis_execution_id=execution_id,
            )
        except Exception as exc:
            raise RhythmSectionTimingReportError(
                f"AD038_CONSTRUCTION_FAILURE:{type(exc).__name__}:{exc}"
            ) from exc
        try:
            profile = self._profile_builder.build(
                all_events,
                localizations,
                assignments,
                temporal_scope=next(iter(scopes)),
                temporal_origin_seconds=0.0,
                execution_id=execution_id,
                provenance_id=provenance_id,
                scientific_authority_ids=("AD-037", "AD-038", "AD-040"),
            )
        except Exception as exc:
            raise RhythmSectionTimingReportError(
                f"AD040_CONSTRUCTION_FAILURE:{type(exc).__name__}:{exc}"
            ) from exc

        content = {
            "schema": {"id": SCHEMA_ID, "version": SCHEMA_VERSION},
            "invocation_authority": {
                "execution_id": execution_id,
                "provenance_id": provenance_id,
                "role_authority_id": role_authority_id,
                "role_authority_fingerprint": role_authority_fingerprint,
                "calibration_authority_id": calibration_authority_id,
                "calibration_authority_fingerprint": (
                    calibration_authority_fingerprint
                ),
                "source_order_rule": "role-label-path-lexicographic/v1",
            },
            "environment": self._environment(jga_revision),
            "source_authorities": authorities,
            "observations": {
                source.label: records for source, _, _, records in analyses
            },
            "elementary_metric_events": [
                self._eme_record(event) for event in sorted(
                    all_events, key=lambda item: (item.timestamp, str(item.id))
                )
            ],
            "ad038_localizations": [
                self._localization_record(item) for item in localizations
            ],
            "ad040_profile": self._profile_record(profile),
            "scientific_status": {
                "evidence": (
                    "PROVENANCE_BOUND_FRAME_RESOLVED_OBSERVATIONS",
                    "NEUTRAL_TEMPORAL_GEOMETRY",
                    "AD_040_RHYTHM_SECTION_TIMING_PROFILE",
                ),
                "default_correspondence_status": "GEOMETRIC_ONLY",
                "calibration": {
                    "applicability": calibration_applicability,
                    "application": "NOT_APPLIED",
                    "correction": "NONE",
                    "authority_id": calibration_authority_id,
                    "authority_fingerprint": calibration_authority_fingerprint,
                },
                "timestamp_correction": "NONE",
                "unsupported_claims": FIREWALL,
            },
            "fingerprint_rule": FINGERPRINT_RULE,
        }
        try:
            fingerprint = sha256(self._canonical_bytes(content)).hexdigest()
            document = {**content, "scientific_fingerprint": fingerprint}
            canonical_json = self._canonical_bytes(document).decode("ascii") + "\n"
        except Exception as exc:
            raise RhythmSectionTimingReportError(
                f"SERIALIZATION_FINGERPRINT_FAILURE:{type(exc).__name__}:{exc}"
            ) from exc
        return RhythmSectionTimingReport(
            schema_id=SCHEMA_ID,
            schema_version=SCHEMA_VERSION,
            scientific_fingerprint=fingerprint,
            canonical_json=canonical_json,
        )

    @staticmethod
    def _validate_invocation(sources, *required_text) -> None:
        if any(not value for value in required_text):
            raise RhythmSectionTimingReportError("MISSING_PROVENANCE_AUTHORITY")
        if not sources:
            raise RhythmSectionTimingReportError("MISSING_SOURCE_AUTHORITY")
        labels = [item.label for item in sources]
        if any(not label.strip() for label in labels):
            raise RhythmSectionTimingReportError("MISSING_SOURCE_LABEL")
        if len(set(labels)) != len(labels):
            raise RhythmSectionTimingReportError("DUPLICATE_SOURCE_LABEL")
        unsupported = [
            item.role for item in sources
            if item.role not in {"TEMPORAL_REFERENCE", "ACCOMPANIMENT"}
        ]
        if unsupported:
            raise RhythmSectionTimingReportError(
                f"UNSUPPORTED_ANALYTICAL_ROLE:{unsupported[0]}"
            )
        references = [item for item in sources if item.role == "TEMPORAL_REFERENCE"]
        if len(references) != 1:
            raise RhythmSectionTimingReportError(
                "ROLE_AUTHORITY_REQUIRES_EXACTLY_ONE_TEMPORAL_REFERENCE"
            )
        if not any(item.role == "ACCOMPANIMENT" for item in sources):
            raise RhythmSectionTimingReportError("MISSING_ACCOMPANIMENT_AUTHORITY")

    @staticmethod
    def _source_authority(source: AuthorizedSourceInput) -> dict:
        path = source.path.expanduser().resolve()
        if not path.exists() or not path.is_file():
            raise RhythmSectionTimingReportError(f"MISSING_SOURCE:{source.label}:{path}")
        try:
            digest_builder = sha256()
            with path.open("rb") as source_file:
                for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                    digest_builder.update(chunk)
            digest = digest_builder.hexdigest()
        except OSError as exc:
            raise RhythmSectionTimingReportError(
                f"UNREADABLE_SOURCE:{source.label}:{path}:{exc}"
            ) from exc
        if source.expected_sha256 is not None and source.expected_sha256 != digest:
            raise RhythmSectionTimingReportError(
                f"SOURCE_CHECKSUM_MISMATCH:{source.label}"
            )
        return {
            "path_used": str(path),
            "label": source.label,
            "role": source.role,
            "sha256": digest,
        }

    @staticmethod
    def _observation_records(context, label: str) -> list[dict]:
        sample_rate = context.audio.sample_rate
        hop = PulseCandidateBuilder.FRAME_LENGTH_SAMPLES
        records = []
        for candidate in sorted(
            context.domain_pulse_candidates,
            key=lambda item: (item.timestamp, str(item.id)),
        ):
            frame = round(candidate.timestamp * sample_rate / hop)
            sample = frame * hop
            reconstructed = sample / sample_rate
            if reconstructed != candidate.timestamp:
                raise RhythmSectionTimingReportError(
                    f"PRODUCER_FRAME_ROUNDTRIP_FAILURE:{label}:{candidate.id}"
                )
            records.append(
                {
                    "pulse_candidate_id": str(candidate.id),
                    "source_identity": str(candidate.sound_source_id),
                    "producer_frame": frame,
                    "producer_sample_coordinate": sample,
                    "timestamp_seconds": candidate.timestamp,
                    "observation_index": candidate.observation_index,
                    "observation_provenance_id": candidate.observation_provenance_id,
                    "frame_coordinate_rule": FRAME_COORDINATE_RULE,
                }
            )
        return records

    @staticmethod
    def _eme_record(event) -> dict:
        return {
            "eme_id": str(event.id),
            "contributor_id": str(event.contributor_id),
            "sound_source_id": str(event.sound_source_id),
            "timestamp_seconds": event.timestamp,
            "supporting_pulse_candidate_ids": tuple(
                str(item) for item in event.supporting_pulse_candidate_ids
            ),
            "materialization_rule": event.materialization_rule,
            "source_asset_sha256": event.source_asset_sha256,
            "temporal_scope": event.temporal_scope,
        }

    @classmethod
    def _drum_reference_record(cls, item):
        if item is None:
            return None
        return {
            "eme_id": str(item.eme_id),
            "source_identity": str(item.sound_source_id),
            "timestamp_seconds": item.timestamp_seconds,
            "supporting_pulse_candidate_ids": tuple(
                str(lineage.pulse_candidate_id) for lineage in item.supporting_observations
            ),
        }

    @classmethod
    def _localization_record(cls, item) -> dict:
        return {
            "target_eme_id": str(item.target_eme_id),
            "target_source_identity": str(item.target_sound_source_id),
            "target_timestamp_seconds": item.target_timestamp_seconds,
            "preceding_reference": cls._drum_reference_record(item.preceding_drum_eme),
            "following_reference": cls._drum_reference_record(item.following_drum_eme),
            "nearest_reference": cls._drum_reference_record(item.nearest_drum_eme),
            "distance_from_preceding_seconds": item.distance_from_preceding_seconds,
            "distance_from_following_seconds": item.distance_from_following_seconds,
            "nearest_displacement_seconds": item.nearest_displacement_seconds,
            "nearest_absolute_displacement_seconds": (
                None if item.nearest_displacement_seconds is None
                else abs(item.nearest_displacement_seconds)
            ),
            "nearest_selection_status": item.nearest_selection_status,
            "observed_interval_fraction": item.observed_interval_fraction,
            "localization_rule": item.localization_rule,
            "analysis_execution_id": item.analysis_execution_id,
            "correspondence_status": "GEOMETRIC_ONLY",
            "calibration_status": "NOT_APPLIED",
        }

    @staticmethod
    def _profile_record(profile) -> dict:
        reference = next(
            item for item in profile.role_assignments
            if item.role == "TEMPORAL_REFERENCE"
        )
        accompaniments = tuple(
            item for item in profile.role_assignments if item.role == "ACCOMPANIMENT"
        )
        role_assignments = [
            {
                "assignment_id": str(item.assignment_id),
                "source_identity": str(item.source_id),
                "asset_id": item.asset_id,
                "temporal_scope": item.temporal_scope,
                "temporal_origin_seconds": item.temporal_origin_seconds,
                "role": item.role,
                "assignment_rule": item.assignment_rule,
                "execution_id": item.execution_id,
                "authority_id": item.scientific_authority_id,
                "authority_fingerprint": item.scientific_authority_fingerprint,
            }
            for item in profile.role_assignments
        ]
        relationships = []
        for item in profile.accompaniment_relationships:
            relation = item.correspondence.authorized_relation
            calibration = item.calibration_evidence
            relationships.append(
                {
                    "target_eme_id": str(item.target_eme.id),
                    "localization_reference": {
                        "target_eme_id": str(
                            item.drum_relative_localization.target_eme_id
                        ),
                        "rule": item.drum_relative_localization.localization_rule,
                        "execution_id": (
                            item.drum_relative_localization.analysis_execution_id
                        ),
                    },
                    "correspondence_status": item.correspondence.status,
                    "authorized_event_relation": (
                        None if relation is None else {
                            "evidence_id": relation.evidence_id,
                            "target_eme_id": str(relation.target_eme_id),
                            "reference_eme_id": str(relation.drum_eme_id),
                            "authority_id": relation.authority_id,
                            "scientific_fingerprint": relation.scientific_fingerprint,
                        }
                    ),
                    "calibration_evidence": (
                        None if calibration is None else {
                            "evidence_id": calibration.evidence_id,
                            "experiment_id": calibration.experiment_id,
                            "scientific_fingerprint": calibration.scientific_fingerprint,
                            "source_pair_type": calibration.source_pair_type,
                            "classification": calibration.classification,
                            "applicability_status": calibration.applicability_status,
                            "applicability_conditions": calibration.applicability_conditions,
                            "uncertainty_evidence_id": calibration.uncertainty_evidence_id,
                        }
                    ),
                    "uncertainty_evidence_id": item.uncertainty_evidence_id,
                }
            )
        return {
            "profile_id": str(profile.profile_id),
            "scientific_fingerprint": profile.scientific_fingerprint,
            "projection_rule": profile.projection_rule,
            "execution_id": profile.execution_id,
            "provenance_id": profile.provenance_id,
            "scientific_authority_ids": profile.scientific_authority_ids,
            "temporal_scope": profile.temporal_scope,
            "temporal_origin_seconds": profile.temporal_origin_seconds,
            "reference_assignment": {
                "assignment_id": str(reference.assignment_id),
                "source_identity": str(reference.source_id),
                "asset_id": reference.asset_id,
                "role": reference.role,
                "authority_id": reference.scientific_authority_id,
                "authority_fingerprint": reference.scientific_authority_fingerprint,
            },
            "accompaniment_assignments": [
                {
                    "assignment_id": str(item.assignment_id),
                    "source_identity": str(item.source_id),
                    "asset_id": item.asset_id,
                    "role": item.role,
                    "authority_id": item.scientific_authority_id,
                    "authority_fingerprint": item.scientific_authority_fingerprint,
                }
                for item in accompaniments
            ],
            "represented_eme_count": (
                len(profile.temporal_reference_events)
                + len(profile.accompaniment_relationships)
            ),
            "temporal_reference_eme_count": len(profile.temporal_reference_events),
            "accompaniment_relationship_count": len(profile.accompaniment_relationships),
            "correspondence_status_counts": {
                "GEOMETRIC_ONLY": len(profile.accompaniment_relationships),
                "AUTHORIZED_EVENT_RELATION": 0,
                "UNRESOLVED": 0,
                "NOT_APPLICABLE": len(profile.temporal_reference_events),
            },
            "calibration_status": "NOT_APPLIED",
            "role_assignments": role_assignments,
            "temporal_reference_eme_ids": tuple(
                str(item.id) for item in profile.temporal_reference_events
            ),
            "relationships": relationships,
        }

    @staticmethod
    def _environment(jga_revision: str) -> dict:
        try:
            jga_version = version("jga")
        except PackageNotFoundError:
            jga_version = "UNKNOWN"
        return {
            "jga_revision": jga_revision,
            "jga_package_version": jga_version,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "numpy_version": numpy.__version__,
            "librosa_version": librosa.__version__,
            "byte_order": sys.byteorder,
        }

    @staticmethod
    def _canonical_bytes(value: dict) -> bytes:
        return json.dumps(
            value,
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
