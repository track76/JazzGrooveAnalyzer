"""Build the minimal read-only AD-040 timing profile by immutable reference."""

from collections.abc import Iterable, Mapping
from hashlib import sha256
import json
from uuid import NAMESPACE_URL, UUID, uuid5

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.representation.drum_relative_eme_localization import (
    DrumRelativeEMELocalization,
)
from jga.representation.rhythm_section_timing_profile import (
    AnalyticalRoleAssignment,
    CalibrationEvidenceReference,
    EventCorrespondence,
    RhythmSectionEventRelationship,
    RhythmSectionTimingProfile,
)


class RhythmSectionTimingProfileBuilder:
    RULE = "rhythm-section-timing-profile/v1"

    def build(
        self,
        events: Iterable[ElementaryMetricEvent],
        drum_relative_localizations: Iterable[DrumRelativeEMELocalization],
        role_assignments: Iterable[AnalyticalRoleAssignment],
        *,
        temporal_scope: str,
        temporal_origin_seconds: float,
        execution_id: str,
        provenance_id: str,
        scientific_authority_ids: Iterable[str],
        correspondence_by_target: Mapping[UUID, EventCorrespondence] | None = None,
        calibration_by_assignment: Mapping[
            UUID, CalibrationEvidenceReference
        ] | None = None,
    ) -> RhythmSectionTimingProfile:
        assignments = tuple(sorted(role_assignments, key=lambda item: str(item.assignment_id)))
        self._validate_assignments(assignments, temporal_scope, temporal_origin_seconds)
        correspondence = correspondence_by_target or {}
        calibration = calibration_by_assignment or {}

        assignment_by_source_asset = {
            (item.source_id, item.asset_id): item for item in assignments
        }
        if len(assignment_by_source_asset) != len(assignments):
            raise ValueError("Role assignments must be unique by source and asset")
        reference_assignment = next(
            item for item in assignments if item.role == "TEMPORAL_REFERENCE"
        )
        accompaniment_assignments = {
            item.assignment_id: item for item in assignments if item.role == "ACCOMPANIMENT"
        }

        ordered_events = tuple(sorted(events, key=lambda item: (item.timestamp, str(item.id))))
        event_by_id = {item.id: item for item in ordered_events}
        if len(event_by_id) != len(ordered_events):
            raise ValueError("Profile input contains duplicate EME identities")
        reference_events = tuple(
            item for item in ordered_events
            if self._assignment_for_event(item, assignment_by_source_asset)
            == reference_assignment
        )

        localizations = tuple(
            sorted(
                drum_relative_localizations,
                key=lambda item: (item.target_timestamp_seconds, str(item.target_eme_id)),
            )
        )
        if len({item.target_eme_id for item in localizations}) != len(localizations):
            raise ValueError("Profile input contains duplicate target localizations")
        reference_event_ids = {item.id for item in reference_events}
        relationships = []
        for localization in localizations:
            target = event_by_id.get(localization.target_eme_id)
            if target is None:
                raise ValueError(f"Missing target EME: {localization.target_eme_id}")
            assignment = self._assignment_for_event(target, assignment_by_source_asset)
            if assignment is None or assignment.role != "ACCOMPANIMENT":
                continue
            event_correspondence = correspondence.get(
                target.id, EventCorrespondence("GEOMETRIC_ONLY")
            )
            relation = event_correspondence.authorized_relation
            if relation is not None:
                if relation.drum_eme_id not in reference_event_ids:
                    raise ValueError("Authorized evidence must identify an in-profile Drum EME")
            calibration_evidence = calibration.get(assignment.assignment_id)
            if calibration_evidence is not None:
                if calibration_evidence.source_role_assignment_id != assignment.assignment_id:
                    raise ValueError("Calibration source assignment mismatch")
                if calibration_evidence.reference_role_assignment_id != reference_assignment.assignment_id:
                    raise ValueError("Calibration reference assignment mismatch")
            relationships.append(
                RhythmSectionEventRelationship(
                    target_eme=target,
                    drum_relative_localization=localization,
                    correspondence=event_correspondence,
                    calibration_evidence=calibration_evidence,
                    uncertainty_evidence_id=(
                        calibration_evidence.uncertainty_evidence_id
                        if calibration_evidence is not None else None
                    ),
                )
            )

        authorities = tuple(sorted(set(scientific_authority_ids)))
        scientific_content = {
            "projection_rule": self.RULE,
            "temporal_scope": temporal_scope,
            "temporal_origin_seconds": temporal_origin_seconds,
            "execution_id": execution_id,
            "provenance_id": provenance_id,
            "authority_ids": authorities,
            "role_assignments": [self._assignment_key(item) for item in assignments],
            "reference_eme_ids": [str(item.id) for item in reference_events],
            "relationships": [self._relationship_key(item) for item in relationships],
        }
        fingerprint = sha256(
            json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return RhythmSectionTimingProfile(
            profile_id=uuid5(NAMESPACE_URL, f"jga:{self.RULE}:{fingerprint}"),
            role_assignments=assignments,
            temporal_scope=temporal_scope,
            temporal_origin_seconds=temporal_origin_seconds,
            temporal_reference_events=reference_events,
            accompaniment_relationships=tuple(relationships),
            projection_rule=self.RULE,
            execution_id=execution_id,
            provenance_id=provenance_id,
            scientific_authority_ids=authorities,
            scientific_fingerprint=fingerprint,
        )

    @staticmethod
    def _assignment_for_event(event, assignments):
        if event.sound_source_id is None or event.source_asset_sha256 is None:
            return None
        return assignments.get((event.sound_source_id, event.source_asset_sha256))

    @staticmethod
    def _validate_assignments(assignments, temporal_scope, temporal_origin):
        references = [item for item in assignments if item.role == "TEMPORAL_REFERENCE"]
        if len(references) != 1:
            raise ValueError("Profile requires exactly one temporal-reference assignment")
        for item in assignments:
            if item.temporal_scope != temporal_scope:
                raise ValueError("Role assignment temporal scope mismatch")
            if item.temporal_origin_seconds != temporal_origin:
                raise ValueError("Role assignment temporal origin mismatch")

    @staticmethod
    def _assignment_key(item):
        return {
            "assignment_id": str(item.assignment_id), "source_id": str(item.source_id),
            "asset_id": item.asset_id, "role": item.role,
            "temporal_scope": item.temporal_scope,
            "temporal_origin_seconds": item.temporal_origin_seconds,
            "assignment_rule": item.assignment_rule, "execution_id": item.execution_id,
            "authority_id": item.scientific_authority_id,
            "authority_fingerprint": item.scientific_authority_fingerprint,
        }

    @staticmethod
    def _relationship_key(item):
        relation = item.correspondence.authorized_relation
        calibration = item.calibration_evidence
        return {
            "target_eme_id": str(item.target_eme.id),
            "localization_key": [
                str(item.drum_relative_localization.target_eme_id),
                item.drum_relative_localization.localization_rule,
                item.drum_relative_localization.analysis_execution_id,
            ],
            "correspondence_status": item.correspondence.status,
            "authorized_relation": None if relation is None else {
                "evidence_id": relation.evidence_id,
                "target_eme_id": str(relation.target_eme_id),
                "drum_eme_id": str(relation.drum_eme_id),
                "authority_id": relation.authority_id,
                "scientific_fingerprint": relation.scientific_fingerprint,
            },
            "calibration_evidence": None if calibration is None else {
                "evidence_id": calibration.evidence_id,
                "experiment_id": calibration.experiment_id,
                "scientific_fingerprint": calibration.scientific_fingerprint,
                "source_pair_type": calibration.source_pair_type,
                "classification": calibration.classification,
                "applicability_status": calibration.applicability_status,
                "applicability_conditions": calibration.applicability_conditions,
                "uncertainty_evidence_id": calibration.uncertainty_evidence_id,
                "source_role_assignment_id": str(calibration.source_role_assignment_id),
                "reference_role_assignment_id": str(calibration.reference_role_assignment_id),
            },
            "uncertainty_evidence_id": item.uncertainty_evidence_id,
        }
