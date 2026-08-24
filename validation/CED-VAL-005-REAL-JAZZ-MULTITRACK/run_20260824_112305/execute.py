"""Execute H-CEDVAL005-REAL-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01."""
from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from decimal import Decimal, getcontext
from hashlib import sha256
import json
import math
import platform
from pathlib import Path
import sys
from uuid import NAMESPACE_URL, uuid5
import wave

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)
from jga.representation.builders.rhythm_section_timing_profile_builder import (
    RhythmSectionTimingProfileBuilder,
)
from jga.representation.rhythm_section_timing_profile import AnalyticalRoleAssignment

getcontext().prec = 50
BASE = Path("validation/CED-VAL-005-REAL-JAZZ-MULTITRACK")
RUN = BASE / "run_20260824_112305"
PREREG = BASE / "preregistrations/H-CEDVAL005-REAL-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01.md"
DATASET_AUTHORITY = BASE / "input_authority_manifest.json"
INPUT_AUTHORITY = BASE / "analytical_input_authority.json"
STUDY_ID = "H-CEDVAL005-REAL-AUDIO-RHYTHM-SECTION-TIMING-PROFILE-01"
EXECUTION_ID = "EXEC-CEDVAL005-REAL-AUDIO-20260824-112305"
DATASET_FP = "d9d6341f837bc5f56054ffd6c91f6be65a7bdbb8043526a9ac70d924a81335af"
INPUT_FP = "08ac45969fc449503f67ea4e8bda77495c4807e9dd0e0adbe0c37c9cb506b876"
PREREG_COMMIT = "430dc202034b10d112bae0364572527297253487"
SR, HOP, FRAME_COUNT = 44100, 512, 10068072
TEMPORAL_SCOPE = "analysis_input"
SOURCES = (
    ("Drums", "TEMPORAL_REFERENCE", "09_Overheads.wav", "0569a396cff95b130042fc71093e8ba3460e3c0fe0034cb86d2158027d585f3a", 2),
    ("Double Bass", "ACCOMPANIMENT", "11_BassDI.wav", "2c4c06b9b5d4b18e00000bc2c036207fc68fb722c5854e0a30107ad4594a910b", 1),
)
REPO_HASHES = {
    str(PREREG): "ee6834c2e957d120e8667fd3b3022922dae3acb4efa0625487675927efd7295c",
    str(INPUT_AUTHORITY): "f8f0d963fc0a6e9455f6f9cb36bb9b046039d0c87d22e83e64bc02a0918864c9",
    str(DATASET_AUTHORITY): "8248368cf1ab4bdb104b5eeff37be0a28a283af68e76e07c8f622a3fbe844b46",
    "src/jga/pipeline/default_analysis_pipeline.py": "04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17",
    "src/jga/domain/services/elementary_metric_event_builder.py": "137e390a69c9361d5cbfd66908256b2417d76c95d503e7ad2c409cd2e1b66cc2",
    "src/jga/representation/builders/drum_relative_eme_localization_builder.py": "bf6d61bf3c2be644047fd81553e68a73bb0b4f95e67535acc010d30e1fc465fd",
    "src/jga/representation/builders/rhythm_section_timing_profile_builder.py": "92c63c2d19045553b09a3ca36ad2321eba348adac4cfd35cde9e3115f5f720c4",
}


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path) -> str:
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value) -> None:
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def verify_authority() -> tuple[dict, dict, dict[str, Path]]:
    for path, expected in REPO_HASHES.items():
        if checksum(path) != expected:
            raise RuntimeError(f"AUTHORITY_CONFLICT repository checksum: {path}")
    dataset = json.loads(DATASET_AUTHORITY.read_text())
    dataset_copy = dict(dataset)
    frozen_dataset_fp = dataset_copy.pop("dataset_fingerprint")
    if frozen_dataset_fp != DATASET_FP or sha256(canonical(dataset_copy)).hexdigest() != DATASET_FP:
        raise RuntimeError("AUTHORITY_CONFLICT dataset fingerprint")
    analytical = json.loads(INPUT_AUTHORITY.read_text())
    analytical_copy = dict(analytical)
    frozen_input_fp = analytical_copy.pop("analytical_input_fingerprint")
    if frozen_input_fp != INPUT_FP or sha256(canonical(analytical_copy)).hexdigest() != INPUT_FP:
        raise RuntimeError("AUTHORITY_CONFLICT analytical-input fingerprint")
    by_source = {item["analytical_source"]: item for item in analytical["selected_inputs"]}
    paths = {}
    for source, role, filename, expected_sha, channels in SOURCES:
        item = by_source[source]
        path = Path(item["absolute_path"])
        if item["filename"] != filename or item["analytical_role"] != role or item["sha256"] != expected_sha:
            raise RuntimeError(f"AUTHORITY_CONFLICT analytical binding: {source}")
        if checksum(path) != expected_sha:
            raise RuntimeError(f"AUTHORITY_CONFLICT raw asset: {source}")
        with wave.open(str(path), "rb") as wav:
            props = (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes(), wav.getcomptype())
        if props != (channels, 3, SR, FRAME_COUNT, "NONE"):
            raise RuntimeError(f"AUTHORITY_CONFLICT WAV properties: {source}: {props}")
        paths[source] = path
    return dataset, analytical, paths


def producer_frame(timestamp: float) -> int:
    frame = round(timestamp * SR / HOP)
    replay = float(librosa.frames_to_time(frame, sr=SR, hop_length=HOP))
    if replay.hex() != timestamp.hex():
        raise RuntimeError(f"FRAME_AUTHORITY_CONFLICT: {timestamp.hex()} != {replay.hex()}")
    return frame


def candidate_record(candidate) -> dict:
    # Strength and confidence are intentionally not read or serialized.
    frame = producer_frame(candidate.timestamp)
    return {
        "pulse_candidate_id": str(candidate.id),
        "sound_source_id": str(candidate.sound_source_id),
        "producer_frame": frame,
        "producer_sample_coordinate": frame * HOP,
        "timestamp_seconds": candidate.timestamp,
        "timestamp_hex": candidate.timestamp.hex(),
        "observation_index": candidate.observation_index,
        "observation_provenance_id": candidate.observation_provenance_id,
    }


def eme_record(event) -> dict:
    frame = producer_frame(event.timestamp)
    return {
        "eme_id": str(event.id),
        "contributor_id": str(event.contributor_id),
        "sound_source_id": str(event.sound_source_id),
        "producer_frame": frame,
        "producer_sample_coordinate": frame * HOP,
        "timestamp_seconds": event.timestamp,
        "timestamp_hex": event.timestamp.hex(),
        "supporting_pulse_candidate_ids": [str(item) for item in event.supporting_pulse_candidate_ids],
        "association_rule": event.association_rule,
        "association_outcome": event.association_outcome,
        "evidence_status": event.evidence_status,
        "materialization_rule": event.materialization_rule,
        "temporal_scope": event.temporal_scope,
        "source_asset_sha256": event.source_asset_sha256,
    }


def reference_record(reference):
    if reference is None:
        return None
    return {
        "eme_id": str(reference.eme_id),
        "contributor_id": str(reference.contributor_id),
        "sound_source_id": str(reference.sound_source_id),
        "timestamp_seconds": reference.timestamp_seconds,
        "timestamp_hex": reference.timestamp_seconds.hex(),
        "supporting_observations": [
            {
                "pulse_candidate_id": str(item.pulse_candidate_id),
                "sound_source_id": str(item.sound_source_id),
                "observation_index": item.observation_index,
                "observation_provenance_id": item.observation_provenance_id,
            }
            for item in reference.supporting_observations
        ],
        "source_asset_sha256": reference.source_asset_sha256,
        "temporal_scope": reference.temporal_scope,
        "materialization_rule": reference.materialization_rule,
    }


def localization_record(item) -> dict:
    stable_key = f"{item.target_eme_id}:{item.localization_rule}:{item.analysis_execution_id}"
    return {
        "localization_id": str(uuid5(NAMESPACE_URL, f"jga:ad038:{stable_key}")),
        "target_eme_id": str(item.target_eme_id),
        "target_timestamp_seconds": item.target_timestamp_seconds,
        "target_timestamp_hex": item.target_timestamp_seconds.hex(),
        "target_contributor_id": str(item.target_contributor_id),
        "target_sound_source_id": str(item.target_sound_source_id),
        "target_source_asset_sha256": item.target_source_asset_sha256,
        "target_temporal_scope": item.target_temporal_scope,
        "target_materialization_rule": item.target_materialization_rule,
        "preceding_drum_reference": reference_record(item.preceding_drum_eme),
        "following_drum_reference": reference_record(item.following_drum_eme),
        "nearest_drum_reference": reference_record(item.nearest_drum_eme),
        "distance_from_preceding_seconds": item.distance_from_preceding_seconds,
        "distance_from_following_seconds": item.distance_from_following_seconds,
        "nearest_signed_displacement_seconds": item.nearest_displacement_seconds,
        "nearest_absolute_displacement_seconds": None if item.nearest_displacement_seconds is None else abs(item.nearest_displacement_seconds),
        "nearest_selection_status": item.nearest_selection_status,
        "relationship_status": "GEOMETRIC_ONLY" if item.nearest_drum_eme is not None else "UNRESOLVED",
        "observed_interval_fraction": item.observed_interval_fraction,
        "temporal_origin_seconds": item.temporal_origin_seconds,
        "localization_rule": item.localization_rule,
        "analysis_execution_id": item.analysis_execution_id,
    }


def quantile(sorted_values: list[float], p: float) -> float:
    position = (len(sorted_values) - 1) * p
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return sorted_values[low]
    fraction = position - low
    return sorted_values[low] * (1.0 - fraction) + sorted_values[high] * fraction


def describe(values: list[float]) -> dict:
    if not values:
        return {"n": 0, "statistics": "NOT_AVAILABLE"}
    ordered = sorted(values)
    mean = math.fsum(ordered) / len(ordered)
    variance = math.fsum((value - mean) ** 2 for value in ordered) / len(ordered)
    stats = {
        "minimum": ordered[0],
        "q1": quantile(ordered, 0.25),
        "median": quantile(ordered, 0.50),
        "q3": quantile(ordered, 0.75),
        "maximum": ordered[-1],
        "mean": mean,
        "population_standard_deviation": math.sqrt(variance),
    }
    return {
        "n": len(ordered),
        "quantile_method": "linear_empirical_interpolation_at_(n-1)*p",
        "seconds": stats,
        "milliseconds": {key: value * 1000.0 for key, value in stats.items()},
    }


def execute_once(paths: dict[str, Path]) -> dict:
    analyses = {source: AnalysisPipeline().analyze(str(path)) for source, path in paths.items()}
    candidates = {}
    events = {}
    runtime_candidates = []
    for source, _role, _filename, expected_sha, _channels in SOURCES:
        context = analyses[source]
        candidate_items = tuple(context.domain_pulse_candidates)
        event_items = tuple(context.elementary_metric_events)
        candidate_by_id = {str(item.id): item for item in candidate_items}
        if len(candidate_by_id) != len(candidate_items):
            raise RuntimeError(f"AD037_AUTHORITY_CONFLICT duplicate candidate identity: {source}")
        if len(event_items) != len(candidate_items):
            raise RuntimeError(f"AD037_AUTHORITY_CONFLICT cardinality: {source}")
        for event in event_items:
            lineage = [str(item) for item in event.supporting_pulse_candidate_ids]
            if len(lineage) != 1 or lineage[0] not in candidate_by_id:
                raise RuntimeError(f"AD037_AUTHORITY_CONFLICT lineage: {event.id}")
            candidate = candidate_by_id[lineage[0]]
            if event.timestamp.hex() != candidate.timestamp.hex():
                raise RuntimeError(f"AD037_AUTHORITY_CONFLICT timestamp: {event.id}")
            if event.source_asset_sha256 != expected_sha:
                raise RuntimeError(f"AD037_AUTHORITY_CONFLICT asset: {event.id}")
        candidates[source] = sorted((candidate_record(item) for item in candidate_items), key=lambda x: (x["producer_frame"], x["pulse_candidate_id"]))
        events[source] = sorted((eme_record(item) for item in event_items), key=lambda x: (x["producer_frame"], x["eme_id"]))
        runtime_candidates.extend(candidate_items)

    drum_events = tuple(analyses["Drums"].elementary_metric_events)
    bass_events = tuple(analyses["Double Bass"].elementary_metric_events)
    localizations = DrumRelativeEMELocalizationBuilder().build(
        bass_events,
        drum_events,
        tuple(runtime_candidates),
        temporal_origin_seconds=0.0,
        analysis_execution_id=EXECUTION_ID,
    )
    localization_records = sorted((localization_record(item) for item in localizations), key=lambda x: (x["target_timestamp_seconds"], x["target_eme_id"]))

    assignments = []
    for source, role, _filename, expected_sha, _channels in SOURCES:
        sample = tuple(analyses[source].elementary_metric_events)[0]
        assignments.append(AnalyticalRoleAssignment(
            assignment_id=uuid5(NAMESPACE_URL, f"{STUDY_ID}:role:{source}:{expected_sha}"),
            source_id=sample.sound_source_id,
            asset_id=expected_sha,
            temporal_scope=TEMPORAL_SCOPE,
            temporal_origin_seconds=0.0,
            role=role,
            assignment_rule="cedval005-pi-approved-analytical-role/v1",
            execution_id=EXECUTION_ID,
            scientific_authority_id="PR-CEDVAL005-ANALYTICAL-INPUTS-001",
            scientific_authority_fingerprint=INPUT_FP,
        ))
    profile = RhythmSectionTimingProfileBuilder().build(
        drum_events + bass_events,
        localizations,
        assignments,
        temporal_scope=TEMPORAL_SCOPE,
        temporal_origin_seconds=0.0,
        execution_id=EXECUTION_ID,
        provenance_id="PR-CED-VAL-005-REAL-JAZZ-MULTITRACK-001",
        scientific_authority_ids=("AD-037", "AD-038", "AD-040", STUDY_ID),
    )
    profile_record = {
        "profile_id": str(profile.profile_id),
        "scientific_fingerprint": profile.scientific_fingerprint,
        "projection_rule": profile.projection_rule,
        "temporal_scope": profile.temporal_scope,
        "temporal_origin_seconds": profile.temporal_origin_seconds,
        "execution_id": profile.execution_id,
        "provenance_id": profile.provenance_id,
        "scientific_authority_ids": list(profile.scientific_authority_ids),
        "role_assignments": [
            {
                "assignment_id": str(item.assignment_id),
                "source_id": str(item.source_id),
                "asset_id": item.asset_id,
                "role": item.role,
                "temporal_scope": item.temporal_scope,
                "temporal_origin_seconds": item.temporal_origin_seconds,
                "assignment_rule": item.assignment_rule,
                "execution_id": item.execution_id,
                "scientific_authority_id": item.scientific_authority_id,
                "scientific_authority_fingerprint": item.scientific_authority_fingerprint,
            }
            for item in profile.role_assignments
        ],
        "temporal_reference_eme_ids": [str(item.id) for item in profile.temporal_reference_events],
        "accompaniment_relationship_target_eme_ids": [str(item.target_eme.id) for item in profile.accompaniment_relationships],
        "represented_observation_count": len(profile.temporal_reference_events) + len(profile.accompaniment_relationships),
        "source_counts": {"Drums": len(profile.temporal_reference_events), "Double Bass": len(profile.accompaniment_relationships)},
        "relationship_status_counts": dict(sorted(Counter(item.correspondence.status for item in profile.accompaniment_relationships).items())),
        "calibration_applicability": "UNESTABLISHED",
    }
    signed = [item["nearest_signed_displacement_seconds"] for item in localization_records if item["nearest_signed_displacement_seconds"] is not None]
    absolute = [abs(item) for item in signed]
    source_summary = {}
    for source in ("Drums", "Double Bass"):
        source_summary[source] = {
            "pulse_candidate_count": len(candidates[source]),
            "eme_count": len(events[source]),
            "producer_frame_scope": None if not events[source] else [events[source][0]["producer_frame"], events[source][-1]["producer_frame"]],
            "timestamp_scope_seconds": None if not events[source] else [events[source][0]["timestamp_seconds"], events[source][-1]["timestamp_seconds"]],
            "timestamp_scope_hex": None if not events[source] else [events[source][0]["timestamp_hex"], events[source][-1]["timestamp_hex"]],
        }
    geometry_summary = {
        "eligible_count": len(bass_events),
        "localized_count": sum(item["nearest_drum_reference"] is not None for item in localization_records),
        "unresolved_count": sum(item["nearest_drum_reference"] is None for item in localization_records),
        "preceding_available_count": sum(item["preceding_drum_reference"] is not None for item in localization_records),
        "following_available_count": sum(item["following_drum_reference"] is not None for item in localization_records),
        "nearest_available_count": sum(item["nearest_drum_reference"] is not None for item in localization_records),
        "nearest_tie_count": sum(item["nearest_selection_status"] == "EQUAL_DISTANCE_TIE" for item in localization_records),
        "nearest_selection_status_counts": dict(sorted(Counter(item["nearest_selection_status"] for item in localization_records).items())),
        "relationship_status_counts": dict(sorted(Counter(item["relationship_status"] for item in localization_records).items())),
        "signed_displacement_seconds": signed,
        "absolute_displacement_seconds": absolute,
        "signed_displacement_descriptive": describe(signed),
        "absolute_displacement_descriptive": describe(absolute),
    }
    return {
        "pulse_candidates_without_strength_or_confidence": candidates,
        "elementary_metric_events": events,
        "drum_relative_localizations": localization_records,
        "rhythm_section_timing_profile": profile_record,
        "source_summary": source_summary,
        "geometry_summary": geometry_summary,
    }


def render_visualization(content: dict) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    events = content["elementary_metric_events"]
    localizations = content["drum_relative_localizations"]
    fig, ax = plt.subplots(figsize=(18, 5.5), constrained_layout=True)
    for event in events["Drums"]:
        ax.scatter(event["timestamp_seconds"], 1.0, s=5, color="#303030", zorder=3)
    for event in events["Double Bass"]:
        ax.scatter(event["timestamp_seconds"], 0.0, s=5, color="#1769aa", zorder=3)
    for item in localizations:
        reference = item["nearest_drum_reference"]
        if reference is not None:
            ax.plot([item["target_timestamp_seconds"], reference["timestamp_seconds"]], [0.0, 1.0], color="#9aa6b2", alpha=0.16, linewidth=0.35, zorder=1)
    ax.set_xlim(0.0, FRAME_COUNT / SR)
    ax.set_ylim(-0.5, 1.5)
    ax.set_yticks([0.0, 1.0], ["Double Bass", "Drums"])
    ax.set_xlabel("Absolute distributed-file time (seconds)")
    ax.set_title("CED-VAL-005 — OBSERVATIONAL / FRAME-RESOLVED\nNeutral AD-038 geometry; NOT physical-onset Ground Truth")
    ax.grid(axis="x", color="#dddddd", linewidth=0.4)
    output = RUN / "rhythm_section_timing_profile.png"
    fig.savefig(output, dpi=180)
    plt.close(fig)
    return output


def main() -> None:
    dataset, analytical, paths = verify_authority()
    first = execute_once(paths)
    second = execute_once(paths)
    if canonical(first) != canonical(second):
        raise RuntimeError("DETERMINISTIC_REPLAY_FAILURE")
    scientific_content = {
        "schema": "JGA-CEDVAL005-REAL-AUDIO-OBSERVATIONAL-RESULT/v1",
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "dataset_authority_id": dataset["authority_id"],
        "dataset_fingerprint": DATASET_FP,
        "analytical_input_authority_id": analytical["authority_id"],
        "analytical_input_fingerprint": INPUT_FP,
        "common_distributed_file_scope": {"sample_rate_hz": SR, "first_frame": 0, "last_frame": FRAME_COUNT - 1, "frame_count": FRAME_COUNT},
        **first,
        "firewalls": {
            "correspondence_status": "GEOMETRIC_ONLY",
            "calibration_applicability": "UNESTABLISHED",
            "h02_used": False,
            "strength_accessed_by_scientific_execution": False,
            "bpm_meter_symbolic_input_used": False,
            "musical_interpretation_performed": False,
            "jga_tuned": False,
            "raw_assets_changed": False,
            "production_code_changed": False,
            "historical_authorities_changed": False,
        },
        "real_audio_limitations": [
            "microphone bleed may be present",
            "Overheads represent the recorded Drum source",
            "BassDI represents the recorded Double Bass source",
            "common hardware acquisition clock is unestablished",
            "simultaneous acquisition is unestablished",
            "absence of editing is unestablished",
            "physical onset is unavailable",
            "sample-accurate human microtiming Ground Truth is unavailable",
            "source isolation is unestablished",
        ],
        "deterministic_replay": "PASS_EXACT_TWO_COMPLETE_EXECUTIONS",
    }
    scientific_fingerprint = sha256(canonical(scientific_content)).hexdigest()
    write_json(RUN / "input_manifest.json", {
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "preregistration_commit": PREREG_COMMIT,
        "dataset_fingerprint": DATASET_FP,
        "analytical_input_fingerprint": INPUT_FP,
        "repository_checksums": REPO_HASHES,
        "raw_asset_checksums": {source: checksum(path) for source, path in paths.items()},
        "environment": {"python": sys.version, "platform": platform.platform(), "librosa": librosa.__version__},
        "authority_gate": "PASS",
    })
    write_json(RUN / "pulse_candidates.json", first["pulse_candidates_without_strength_or_confidence"])
    write_json(RUN / "elementary_metric_events.json", first["elementary_metric_events"])
    write_json(RUN / "drum_relative_localizations.json", first["drum_relative_localizations"])
    write_json(RUN / "rhythm_section_timing_profile.json", first["rhythm_section_timing_profile"])
    write_json(RUN / "source_summary.json", first["source_summary"])
    write_json(RUN / "geometry_summary.json", first["geometry_summary"])
    write_json(RUN / "scientific_content.json", scientific_content)
    visualization = render_visualization(first)
    result = {
        "status": "PASS_FROZEN_REAL_AUDIO_OBSERVATIONAL_PROFILE",
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "scientific_fingerprint": scientific_fingerprint,
        "profile_id": first["rhythm_section_timing_profile"]["profile_id"],
        "profile_fingerprint": first["rhythm_section_timing_profile"]["scientific_fingerprint"],
        "source_summary": first["source_summary"],
        "geometry_summary": first["geometry_summary"],
        "deterministic_replay": "PASS_EXACT_TWO_COMPLETE_EXECUTIONS",
        "visualization": str(visualization),
        "firewalls": scientific_content["firewalls"],
    }
    write_json(RUN / "result.json", result)
    write_json(RUN / "completion_protocol.json", {
        "study_id": STUDY_ID,
        "status": result["status"],
        "authority_gate": "PASS",
        "ad037_cardinality_and_lineage": "PASS",
        "ad038_geometry": "PASS",
        "ad040_profile": "PASS",
        "deterministic_replay": result["deterministic_replay"],
        "scientific_fingerprint": scientific_fingerprint,
    })
    report = [
        f"# {STUDY_ID} Frozen Result",
        "",
        f"Status: **{result['status']}**",
        "",
        f"Scientific fingerprint: `{scientific_fingerprint}`.",
        "",
        "The unchanged AD-037/AD-038/AD-040 stack produced an observational, frame-resolved profile on the common distributed-file coordinate. Correspondence remains `GEOMETRIC_ONLY`; calibration applicability remains `UNESTABLISHED`.",
        "",
        "No BPM, meter, symbolic input, H02, strength analysis, calibration correction or musical interpretation was used. Real-audio authority limitations remain unchanged.",
    ]
    (RUN / "report.md").write_text("\n".join(report) + "\n")
    artifacts = [
        "execute.py", "input_manifest.json", "pulse_candidates.json",
        "elementary_metric_events.json", "drum_relative_localizations.json",
        "rhythm_section_timing_profile.json", "source_summary.json",
        "geometry_summary.json", "scientific_content.json", "result.json",
        "completion_protocol.json", "report.md", visualization.name,
    ]
    write_json(RUN / "artifact_manifest.json", {
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "scientific_fingerprint": scientific_fingerprint,
        "artifacts": {name: checksum(RUN / name) for name in artifacts},
    })
    print(json.dumps({
        "status": result["status"],
        "scientific_fingerprint": scientific_fingerprint,
        "profile_id": result["profile_id"],
        "profile_fingerprint": result["profile_fingerprint"],
        "source_summary": result["source_summary"],
        "geometry_summary": result["geometry_summary"],
        "visualization": result["visualization"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
