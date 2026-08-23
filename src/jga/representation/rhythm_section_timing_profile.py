"""Immutable AD-040 Rhythm Section Timing Profile references."""

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from jga.domain.elementary_metric_event import ElementaryMetricEvent
from jga.representation.drum_relative_eme_localization import (
    DrumRelativeEMELocalization,
)


AnalyticalRole = Literal[
    "TEMPORAL_REFERENCE",
    "ACCOMPANIMENT",
    "OUTSIDE_CURRENT_CORE",
    "DEFERRED",
]
CorrespondenceStatus = Literal[
    "GEOMETRIC_ONLY",
    "AUTHORIZED_EVENT_RELATION",
    "UNRESOLVED",
    "NOT_APPLICABLE",
]
CalibrationApplicabilityStatus = Literal[
    "APPLICABLE",
    "INSUFFICIENT_EVIDENCE",
    "NOT_APPLICABLE",
]
ANALYTICAL_ROLES = frozenset(
    {"TEMPORAL_REFERENCE", "ACCOMPANIMENT", "OUTSIDE_CURRENT_CORE", "DEFERRED"}
)
CORRESPONDENCE_STATUSES = frozenset(
    {"GEOMETRIC_ONLY", "AUTHORIZED_EVENT_RELATION", "UNRESOLVED", "NOT_APPLICABLE"}
)
CALIBRATION_APPLICABILITY_STATUSES = frozenset(
    {"APPLICABLE", "INSUFFICIENT_EVIDENCE", "NOT_APPLICABLE"}
)


@dataclass(frozen=True, slots=True)
class AnalyticalRoleAssignment:
    assignment_id: UUID
    source_id: UUID
    asset_id: str
    temporal_scope: str
    temporal_origin_seconds: float
    role: AnalyticalRole
    assignment_rule: str
    execution_id: str
    scientific_authority_id: str
    scientific_authority_fingerprint: str

    def __post_init__(self) -> None:
        if self.role not in ANALYTICAL_ROLES:
            raise ValueError(f"Unsupported analytical role: {self.role}")
        if not self.asset_id:
            raise ValueError("Role assignment requires asset identity")
        if not self.temporal_scope:
            raise ValueError("Role assignment requires temporal scope")
        if not self.assignment_rule or not self.execution_id:
            raise ValueError("Role assignment requires rule and execution identity")
        if not self.scientific_authority_id or not self.scientific_authority_fingerprint:
            raise ValueError("Role assignment requires scientific authority")


@dataclass(frozen=True, slots=True)
class AuthorizedEventRelationReference:
    evidence_id: str
    target_eme_id: UUID
    drum_eme_id: UUID
    authority_id: str
    scientific_fingerprint: str


@dataclass(frozen=True, slots=True)
class EventCorrespondence:
    status: CorrespondenceStatus
    authorized_relation: AuthorizedEventRelationReference | None = None

    def __post_init__(self) -> None:
        if self.status not in CORRESPONDENCE_STATUSES:
            raise ValueError(f"Unsupported correspondence status: {self.status}")
        has_authority = self.authorized_relation is not None
        if self.status == "AUTHORIZED_EVENT_RELATION" and not has_authority:
            raise ValueError("Authorized relation requires independent evidence")
        if self.status != "AUTHORIZED_EVENT_RELATION" and has_authority:
            raise ValueError("Independent relation evidence requires authorized status")


@dataclass(frozen=True, slots=True)
class CalibrationEvidenceReference:
    evidence_id: str
    experiment_id: str
    scientific_fingerprint: str
    source_pair_type: str
    classification: str
    applicability_status: CalibrationApplicabilityStatus
    applicability_conditions: tuple[str, ...]
    uncertainty_evidence_id: str | None
    source_role_assignment_id: UUID
    reference_role_assignment_id: UUID

    def __post_init__(self) -> None:
        if self.applicability_status not in CALIBRATION_APPLICABILITY_STATUSES:
            raise ValueError(
                f"Unsupported calibration applicability: {self.applicability_status}"
            )


@dataclass(frozen=True, slots=True)
class RhythmSectionEventRelationship:
    """References raw authority; contains no copied or corrected timing values."""

    target_eme: ElementaryMetricEvent
    drum_relative_localization: DrumRelativeEMELocalization
    correspondence: EventCorrespondence
    calibration_evidence: CalibrationEvidenceReference | None
    uncertainty_evidence_id: str | None

    def __post_init__(self) -> None:
        if self.target_eme.id != self.drum_relative_localization.target_eme_id:
            raise ValueError("Localization must reference the target EME")
        relation = self.correspondence.authorized_relation
        if relation is not None:
            if relation.target_eme_id != self.target_eme.id:
                raise ValueError("Authorized evidence must identify the target EME")


@dataclass(frozen=True, slots=True)
class RhythmSectionTimingProfile:
    profile_id: UUID
    role_assignments: tuple[AnalyticalRoleAssignment, ...]
    temporal_scope: str
    temporal_origin_seconds: float
    temporal_reference_events: tuple[ElementaryMetricEvent, ...]
    accompaniment_relationships: tuple[RhythmSectionEventRelationship, ...]
    projection_rule: str
    execution_id: str
    provenance_id: str
    scientific_authority_ids: tuple[str, ...]
    scientific_fingerprint: str
