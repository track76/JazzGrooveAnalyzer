"""Blind out-of-sample execution of frozen H02 on corrected CED-VAL-002."""

from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import DrumRelativeEMELocalizationBuilder
from jga.representation.builders.rhythm_section_timing_profile_builder import RhythmSectionTimingProfileBuilder
from jga.representation.rhythm_section_timing_profile import AnalyticalRoleAssignment


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
EXTERNAL = Path("/Volumes/SSD Track/JGA/datasets/CED-VAL-002-SWING")
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-02.md"
DATASET_MANIFEST = ROOT / "validation/CED-VAL-002-SWING/input_authority_manifest_v2_corrected.json"
SOURCES = (
    ("Drums", EXTERNAL / "steams/CED-VAL-002-swing_drums.wav", 192, "TEMPORAL_REFERENCE", "f3f75d95b05e7710dce5c35b68a7c54f2241a3d24177fc92f723b2ddeccbfbbb"),
    ("Double Bass", EXTERNAL / "steams/CED-VAL-002-swing_bass.wav", 127, "ACCOMPANIMENT", "dc71100c99526bbb6c1d4a6626cacae55db3d434a8cfc1216dfeda15a65549d4"),
    ("Piano", EXTERNAL / "steams/CED-VAL-002-swing_piano.wav", 63, "ACCOMPANIMENT", "4d2b03e7740d7487c365b2049959dd5cdc4f3b623fa9a4497bc698201c9bd75a"),
)
EXPECTED = {
    "preregistration_sha256": "10f4f445b257a42e0bdb7cd98277ebbd6689c0f76315c04ca115b0f875e50784",
    "dataset_manifest_sha256": "4df994383109bf55f9543961e73db462f061250e3b59e33a4a05b2f7dd5d8552",
    "dataset_fingerprint": "631eaf017cfaf335ee2945bfbe0df19221a0a0d069fee3602880eda7a851ade1",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical(value) -> bytes:
    def convert(item):
        if isinstance(item, dict):
            return {key: convert(val) for key, val in item.items()}
        if isinstance(item, (tuple, list)):
            return [convert(val) for val in item]
        if item.__class__.__name__ == "UUID":
            return str(item)
        return item
    return json.dumps(convert(value), sort_keys=True, separators=(",", ":")).encode()


def event_record(event, frame: int) -> dict:
    return {"eme_id": str(event.id), "timestamp_seconds": event.timestamp, "timestamp_hex": event.timestamp.hex(), "frame": frame, "contributor_id": str(event.contributor_id), "sound_source_id": str(event.sound_source_id), "source_asset_sha256": event.source_asset_sha256, "supporting_pulse_candidate_ids": [str(item) for item in event.supporting_pulse_candidate_ids], "temporal_scope": event.temporal_scope, "materialization_rule": event.materialization_rule}


def predicates(record: dict) -> dict:
    failures = set(record["failure_reasons"])
    target_unique = not any(item.startswith("TARGET_TO_DRUM") for item in failures)
    reverse_unique = "DRUM_TO_TARGET_NEAREST_NOT_UNIQUE" not in failures
    return {"valid_accompaniment_signature": record["target_signature"] is not None, "unique_target_to_drum": target_unique, "unique_drum_to_target": reverse_unique, "mutual_unique_nearest": target_unique and reverse_unique, "recurrent_drum_signature": record["drum_signature"] is not None and record["drum_signature_recurrence"] >= 2, "recurrent_accompaniment_signature": record["target_signature"] is not None and record["target_signature_recurrence"] >= 2, "complete_final_criterion": record["status"] == "BLIND_CANDIDATE"}


def gate_counts(records: list[dict]) -> dict:
    order = ("valid_accompaniment_signature", "unique_target_to_drum", "unique_drum_to_target", "mutual_unique_nearest", "recurrent_drum_signature", "recurrent_accompaniment_signature", "complete_final_criterion")
    tests = [predicates(record) for record in records]
    independent = {gate: sum(item[gate] for item in tests) for gate in order}
    alive = [True] * len(records)
    cumulative = {}
    for gate in order:
        alive = [survives and item[gate] for survives, item in zip(alive, tests)]
        cumulative[gate] = sum(alive)
    return {"independent": independent, "cumulative": cumulative}


def build_once() -> dict:
    checks = {"preregistration_sha256": digest(PREREG), "dataset_manifest_sha256": digest(DATASET_MANIFEST)}
    manifest = json.loads(DATASET_MANIFEST.read_text())
    checks["dataset_fingerprint"] = manifest["dataset_fingerprint"]
    checks["asset_sha256"] = {name: digest(path) for name, path, *_ in SOURCES}
    if any(checks[key] != EXPECTED[key] for key in EXPECTED):
        raise RuntimeError(f"frozen authority mismatch: {checks}")
    for name, _path, _count, _role, expected_sha in SOURCES:
        if checks["asset_sha256"][name] != expected_sha:
            raise RuntimeError(f"asset authority mismatch: {name}")

    analyses = {name: AnalysisPipeline().analyze(str(path)) for name, path, *_ in SOURCES}
    populations = {name: tuple(analyses[name].elementary_metric_events) for name, *_ in SOURCES}
    for name, _path, expected_count, _role, expected_sha in SOURCES:
        events = populations[name]
        if len(events) != expected_count or {item.source_asset_sha256 for item in events} != {expected_sha}:
            raise RuntimeError(f"observed population authority mismatch: {name}")

    all_events = tuple(event for population in populations.values() for event in population)
    all_candidates = tuple(candidate for analysis in analyses.values() for candidate in analysis.domain_pulse_candidates)
    localizations = DrumRelativeEMELocalizationBuilder().build(populations["Double Bass"] + populations["Piano"], populations["Drums"], all_candidates, temporal_origin_seconds=0.0, analysis_execution_id="H02-CEDVAL002-BLIND")
    assignments = []
    for name, _path, _count, role, _sha in SOURCES:
        sample = populations[name][0]
        assignments.append(AnalyticalRoleAssignment(assignment_id=uuid5(NAMESPACE_URL, f"CED-VAL-002-controlled-role:{name}"), source_id=sample.sound_source_id, asset_id=sample.source_asset_sha256, temporal_scope=sample.temporal_scope, temporal_origin_seconds=0.0, role=role, assignment_rule="pi-authorized-controlled-role/v1", execution_id="H02-CEDVAL002-BLIND", scientific_authority_id="AD-040", scientific_authority_fingerprint="b8983e8"))
    profile = RhythmSectionTimingProfileBuilder().build(all_events, localizations, assignments, temporal_scope=all_events[0].temporal_scope, temporal_origin_seconds=0.0, execution_id="H02-CEDVAL002-BLIND", provenance_id="PR-CED-VAL-002-SWING-002", scientific_authority_ids=("AD-037", "AD-038", "AD-040"))

    max_frame = int(max(event.timestamp for event in all_events) * 44100 / 512) + 2
    frame_by_hex = defaultdict(list)
    for frame in range(max_frame + 1):
        frame_by_hex[float(librosa.frames_to_time(frame, sr=44100, hop_length=512)).hex()].append(frame)
    frames = {}
    for event in all_events:
        matches = frame_by_hex[event.timestamp.hex()]
        if len(matches) != 1:
            raise RuntimeError(f"INSUFFICIENT_FRAME_AUTHORITY:{event.id}:{matches}")
        frames[event.id] = matches[0]

    ordered = {name: tuple(sorted(events, key=lambda event: (frames[event.id], str(event.id)))) for name, events in populations.items()}
    signatures = {name: {} for name in ordered}
    support = {name: defaultdict(list) for name in ordered}
    invalid = {name: {} for name in ordered}
    for name, events in ordered.items():
        counts = Counter(frames[event.id] for event in events)
        for index, event in enumerate(events):
            if index == 0 or index == len(events) - 1:
                invalid[name][event.id] = "BOUNDARY"
                continue
            previous, following = events[index - 1], events[index + 1]
            relevant = (frames[previous.id], frames[event.id], frames[following.id])
            if any(counts[value] != 1 for value in relevant):
                invalid[name][event.id] = "DUPLICATE_FRAME_AMBIGUITY"
                continue
            signature = (frames[event.id] - frames[previous.id], frames[following.id] - frames[event.id])
            if signature[0] <= 0 or signature[1] <= 0:
                invalid[name][event.id] = "NON_POSITIVE_INTERVAL"
                continue
            signatures[name][event.id] = signature
            support[name][signature].append(event.id)

    localization_by_target = {item.target_eme_id: item for item in localizations}
    records = []
    for source in ("Double Bass", "Piano"):
        source_events, drums = ordered[source], ordered["Drums"]
        for target in source_events:
            failures = []
            localization = localization_by_target[target.id]
            drum = None
            if localization.nearest_selection_status != "UNIQUE" or localization.nearest_drum_eme is None:
                failures.append("TARGET_TO_DRUM_NEAREST_NOT_UNIQUE")
            else:
                drum = next(item for item in drums if item.id == localization.nearest_drum_eme.eme_id)
                distances = {item.id: abs(target.timestamp - item.timestamp) for item in drums}
                minimum = min(distances.values())
                if [identity for identity, value in distances.items() if value == minimum] != [drum.id]:
                    failures.append("TARGET_TO_DRUM_ARITHMETIC_NOT_UNIQUE")
                reverse = {item.id: abs(drum.timestamp - item.timestamp) for item in source_events}
                reverse_minimum = min(reverse.values())
                if [identity for identity, value in reverse.items() if value == reverse_minimum] != [target.id]:
                    failures.append("DRUM_TO_TARGET_NEAREST_NOT_UNIQUE")
            target_signature = signatures[source].get(target.id)
            drum_signature = None if drum is None else signatures["Drums"].get(drum.id)
            if target_signature is None:
                failures.append(f"TARGET_SIGNATURE_{invalid[source][target.id]}")
            elif len(support[source][target_signature]) < 2:
                failures.append("TARGET_SIGNATURE_NOT_RECURRENT")
            if drum is not None:
                if drum_signature is None:
                    failures.append(f"DRUM_SIGNATURE_{invalid['Drums'][drum.id]}")
                elif len(support["Drums"][drum_signature]) < 2:
                    failures.append("DRUM_SIGNATURE_NOT_RECURRENT")
            record = {"contributor": source, "target": event_record(target, frames[target.id]), "drum": None if drum is None else event_record(drum, frames[drum.id]), "target_signature": target_signature, "drum_signature": drum_signature, "target_signature_recurrence": 0 if target_signature is None else len(support[source][target_signature]), "drum_signature_recurrence": 0 if drum_signature is None else len(support["Drums"][drum_signature]), "nearest_selection_status": localization.nearest_selection_status, "raw_geometric_displacement_seconds": localization.nearest_displacement_seconds, "status": "BLIND_CANDIDATE" if not failures else "UNRESOLVED", "failure_reasons": sorted(set(failures))}
            records.append(record)
    records.sort(key=lambda item: (item["contributor"], item["target"]["frame"], item["target"]["eme_id"]))
    candidates = [record for record in records if record["status"] == "BLIND_CANDIDATE"]
    unresolved = [record for record in records if record["status"] == "UNRESOLVED"]
    content = {"schema": "H02-CEDVAL002-out-of-sample-blind/v1", "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02", "validation_dataset": "PR-CED-VAL-002-SWING-002", "epistemic_status": "BLIND_FROZEN_NO_GROUND_TRUTH_ACCESS", "frozen_h02_preregistration": {"commit": "ca9683c786b8dbf57ea78f07ee16c86a896e3dbc", "sha256": checks["preregistration_sha256"]}, "authority_checks": checks, "configuration": {"sample_rate": 44100, "hop_length": 512, "calibration_values_consumed": False, "ground_truth_consumed": False}, "profile": {"profile_id": str(profile.profile_id), "scientific_fingerprint": profile.scientific_fingerprint}, "population_counts": {name: len(events) for name, events in populations.items()}, "frame_inventory": {name: [event_record(event, frames[event.id]) for event in events] for name, events in ordered.items()}, "signature_inventory": {name: [{"eme_id": str(event.id), "signature": signatures[name].get(event.id), "invalid_reason": invalid[name].get(event.id)} for event in events] for name, events in ordered.items()}, "recurrence_inventory": {name: [{"signature": signature, "count": len(ids), "center_eme_ids": sorted(map(str, ids))} for signature, ids in sorted(source_support.items())] for name, source_support in support.items()}, "candidates": candidates, "unresolved": unresolved, "gate_counts": {source: gate_counts([record for record in records if record["contributor"] == source]) for source in ("Piano", "Double Bass")}}
    content["summary"] = {"candidate_counts": {source: sum(item["contributor"] == source for item in candidates) for source in ("Piano", "Double Bass")}, "candidate_total": len(candidates), "unresolved_counts": {source: sum(item["contributor"] == source for item in unresolved) for source in ("Piano", "Double Bass")}, "unresolved_total": len(unresolved), "failure_reason_counts": dict(sorted(Counter(reason for item in unresolved for reason in item["failure_reasons"]).items()))}
    return content


def main() -> None:
    first, second = build_once(), build_once()
    if canonical(first) != canonical(second):
        raise RuntimeError("deterministic blind replay failed")
    fingerprint = sha256(canonical(first)).hexdigest()
    envelope = {"blind_scientific_fingerprint": fingerprint, "deterministic_replay": True, "scientific_content": first}
    output = RUN / "blind_result.json"
    output.write_bytes(canonical(envelope) + b"\n")
    blind_manifest = {"experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02", "validation_dataset": "PR-CED-VAL-002-SWING-002", "phase": "BLIND_FROZEN", "blind_result_sha256": digest(output), "blind_scientific_fingerprint": fingerprint, "ground_truth_accessed": False, "calibration_values_consumed": False, "deterministic_replay": True}
    (RUN / "blind_manifest.json").write_bytes(canonical(blind_manifest) + b"\n")
    print(json.dumps({**first["summary"], "gate_counts": first["gate_counts"], **blind_manifest}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
