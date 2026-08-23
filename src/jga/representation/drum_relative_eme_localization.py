"""Immutable neutral localization of one non-Drum EME on the audio timeline."""

from dataclasses import dataclass
from typing import Literal
from uuid import UUID


NearestSelectionStatus = Literal[
    "UNIQUE",
    "EQUAL_DISTANCE_TIE",
    "NOT_PRODUCED",
]


@dataclass(frozen=True, slots=True)
class ObservationLineage:
    pulse_candidate_id: UUID
    sound_source_id: UUID
    observation_index: int | None
    observation_provenance_id: str | None


@dataclass(frozen=True, slots=True)
class DrumEMEReference:
    eme_id: UUID
    contributor_id: UUID
    sound_source_id: UUID
    timestamp_seconds: float
    supporting_observations: tuple[ObservationLineage, ...]
    source_asset_sha256: str | None
    temporal_scope: str
    materialization_rule: str


@dataclass(frozen=True, slots=True)
class DrumRelativeEMELocalization:
    target_eme_id: UUID
    target_timestamp_seconds: float
    target_contributor_id: UUID
    target_sound_source_id: UUID
    target_supporting_observations: tuple[ObservationLineage, ...]
    target_source_asset_sha256: str | None
    target_temporal_scope: str
    target_materialization_rule: str

    preceding_drum_eme: DrumEMEReference | None
    following_drum_eme: DrumEMEReference | None
    distance_from_preceding_seconds: float | None
    distance_from_following_seconds: float | None
    nearest_drum_eme: DrumEMEReference | None
    nearest_displacement_seconds: float | None
    nearest_selection_status: NearestSelectionStatus
    observed_interval_fraction: float | None

    temporal_origin_seconds: float
    localization_rule: str
    analysis_execution_id: str

    @property
    def distance_from_preceding_ms(self) -> float | None:
        value = self.distance_from_preceding_seconds
        return None if value is None else value * 1000.0

    @property
    def distance_from_following_ms(self) -> float | None:
        value = self.distance_from_following_seconds
        return None if value is None else value * 1000.0

    @property
    def nearest_displacement_ms(self) -> float | None:
        value = self.nearest_displacement_seconds
        return None if value is None else value * 1000.0
