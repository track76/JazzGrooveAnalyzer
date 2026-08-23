"""Blind phase for H-VAL001-RHYTHM-CORRESPONDENCE-01.

This module deliberately has no symbolic/Ground Truth input or scoring code.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
from hashlib import sha256
import json
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline
from jga.representation.builders.drum_relative_eme_localization_builder import (
    DrumRelativeEMELocalizationBuilder,
)
from jga.representation.builders.rhythm_section_timing_profile_builder import (
    RhythmSectionTimingProfileBuilder,
)
from jga.representation.rhythm_section_timing_profile import AnalyticalRoleAssignment


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
BLIND_INPUT = ROOT / "validation/VAL-001/run_20260816_192519/blind_input.json"
AD038_RESULT = ROOT / "validation/VAL-001/run_20260823_060808/result.json"
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-01.md"
SOURCES = (
    ("Drums", "drums.wav", 63, "TEMPORAL_REFERENCE"),
    ("Double Bass", "double_bass.wav", 27, "ACCOMPANIMENT"),
    ("Piano", "piano.wav", 49, "ACCOMPANIMENT"),
)
EXPECTED = {
    "blind_input_sha256": "25ee4d610f6a3130f0b4f001b1908c8dad443d34ee30413905f6fd377202c9e8",
    "blind_source_record_sha256": "04468297cb6bf70e56af00d73c4071a96fabc429cfbabad1f81e302e7088ca02",
    "ad038_sha256": "92baa58ed69032af8f6ef59b94e36bd7504774e947a96a7ada174658b82a1da7",
    "ad038_fingerprint": "92a6b2e467d0b0b7fe465e9ccb8d9eb6d6e03ed9fb3e7435a2f0fd53bb4c2c62",
    "prereg_sha256": "a28e025b07c8a3d356481bac427a97e029f8b130bb4fe084017c88b5a112d873",
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


def event_record(event, frame):
    return {
        "eme_id": str(event.id),
        "timestamp_seconds": event.timestamp,
        "timestamp_hex": event.timestamp.hex(),
        "frame": frame,
        "contributor_id": str(event.contributor_id),
        "sound_source_id": str(event.sound_source_id),
        "source_asset_sha256": event.source_asset_sha256,
        "supporting_pulse_candidate_ids": [str(item) for item in event.supporting_pulse_candidate_ids],
        "temporal_scope": event.temporal_scope,
        "materialization_rule": event.materialization_rule,
    }


def build_once():
    checks = {
        "blind_input_sha256": digest(BLIND_INPUT),
        "ad038_sha256": digest(AD038_RESULT),
        "prereg_sha256": digest(PREREG),
    }
    blind = json.loads(BLIND_INPUT.read_text())
    ad038 = json.loads(AD038_RESULT.read_text())
    checks["blind_source_record_sha256"] = blind["source_record_sha256"]
    checks["ad038_fingerprint"] = ad038["scientific_fingerprint"]
    if any(checks[key] != EXPECTED[key] for key in checks):
        raise RuntimeError(f"Frozen authority mismatch: {checks}")
    if blind["sample_rate"] != 44100 or blind["frame_length_samples"] != 512:
        raise RuntimeError("Frozen observation configuration mismatch")

    analyses = {
        name: AnalysisPipeline().analyze(ROOT / f"recordings/validation/stems/{filename}")
        for name, filename, _, _ in SOURCES
    }
    populations = {name: tuple(analyses[name].elementary_metric_events) for name, *_ in SOURCES}
    for name, _, expected_count, _ in SOURCES:
        runtime = populations[name]
        frozen = blind["populations"][name]
        if len(runtime) != expected_count or frozen["eme_count"] != expected_count:
            raise RuntimeError(f"Population count mismatch: {name}")
        frozen_ids = {item["eme_id"] for item in frozen["events"]}
        runtime_ids = {str(item.id) for item in runtime}
        if frozen_ids != runtime_ids:
            raise RuntimeError(f"Population identity mismatch: {name}")
        if {item.source_asset_sha256 for item in runtime} != {
            item["source_asset_sha256"] for item in frozen["events"]
        }:
            raise RuntimeError(f"Asset authority mismatch: {name}")

    all_events = tuple(event for source in populations.values() for event in source)
    all_candidates = tuple(
        candidate for analysis in analyses.values() for candidate in analysis.domain_pulse_candidates
    )
    localizations = DrumRelativeEMELocalizationBuilder().build(
        populations["Double Bass"] + populations["Piano"], populations["Drums"],
        all_candidates, temporal_origin_seconds=0.0,
        analysis_execution_id="H-VAL001-RHYTHM-CORRESPONDENCE-01",
    )
    assignments = []
    for name, _, _, role in SOURCES:
        sample = populations[name][0]
        assignments.append(AnalyticalRoleAssignment(
            assignment_id=uuid5(NAMESPACE_URL, f"controlled-role:{name}"),
            source_id=sample.sound_source_id, asset_id=sample.source_asset_sha256,
            temporal_scope=sample.temporal_scope, temporal_origin_seconds=0.0,
            role=role, assignment_rule="pi-authorized-controlled-role/v1",
            execution_id="controlled-role-execution", scientific_authority_id="AD-040",
            scientific_authority_fingerprint="b8983e8",
        ))
    profile = RhythmSectionTimingProfileBuilder().build(
        all_events, localizations, assignments,
        temporal_scope=all_events[0].temporal_scope, temporal_origin_seconds=0.0,
        execution_id="controlled-profile", provenance_id="CED-VAL-001",
        scientific_authority_ids=("AD-037", "AD-038", "AD-040"),
    )
    # Enumerate the declared scope and match exact producer IEEE-754 values.
    max_timestamp = max(event.timestamp for event in all_events)
    max_frame = int(max_timestamp * 44100 / 512) + 2
    frame_by_hex = {}
    for frame in range(max_frame + 1):
        value = float(librosa.frames_to_time(frame, sr=44100, hop_length=512))
        frame_by_hex.setdefault(value.hex(), []).append(frame)
    frames = {}
    for event in all_events:
        matches = frame_by_hex.get(event.timestamp.hex(), [])
        if len(matches) != 1:
            raise RuntimeError(f"INSUFFICIENT_FRAME_AUTHORITY:{event.id}:{matches}")
        frames[event.id] = matches[0]

    ordered = {
        name: tuple(sorted(events, key=lambda event: (frames[event.id], str(event.id))))
        for name, events in populations.items()
    }
    signatures = {name: {} for name in ordered}
    signature_support = {name: defaultdict(list) for name in ordered}
    invalid_signature_reason = {name: {} for name in ordered}
    for name, events in ordered.items():
        counts_by_frame = Counter(frames[event.id] for event in events)
        for index, event in enumerate(events):
            if index == 0 or index == len(events) - 1:
                invalid_signature_reason[name][event.id] = "BOUNDARY"
                continue
            previous, following = events[index - 1], events[index + 1]
            relevant_frames = (frames[previous.id], frames[event.id], frames[following.id])
            if any(counts_by_frame[value] != 1 for value in relevant_frames):
                invalid_signature_reason[name][event.id] = "DUPLICATE_FRAME_AMBIGUITY"
                continue
            signature = (frames[event.id] - frames[previous.id], frames[following.id] - frames[event.id])
            if signature[0] <= 0 or signature[1] <= 0:
                invalid_signature_reason[name][event.id] = "NON_POSITIVE_INTERVAL"
                continue
            signatures[name][event.id] = signature
            signature_support[name][signature].append(event.id)

    localization_by_target = {item.target_eme_id: item for item in localizations}
    unresolved, candidates = [], []
    for source in ("Double Bass", "Piano"):
        source_events = ordered[source]
        drums = ordered["Drums"]
        for target in source_events:
            failures = []
            localization = localization_by_target[target.id]
            drum = None
            if localization.nearest_selection_status != "UNIQUE" or localization.nearest_drum_eme is None:
                failures.append("TARGET_TO_DRUM_NEAREST_NOT_UNIQUE")
            else:
                drum_id = localization.nearest_drum_eme.eme_id
                drum = next(item for item in drums if item.id == drum_id)
                distances = {item.id: abs(target.timestamp - item.timestamp) for item in drums}
                minimum = min(distances.values())
                if [key for key, value in distances.items() if value == minimum] != [drum.id]:
                    failures.append("TARGET_TO_DRUM_ARITHMETIC_NOT_UNIQUE")
                reverse = {item.id: abs(drum.timestamp - item.timestamp) for item in source_events}
                reverse_minimum = min(reverse.values())
                if [key for key, value in reverse.items() if value == reverse_minimum] != [target.id]:
                    failures.append("DRUM_TO_TARGET_NEAREST_NOT_UNIQUE")
            target_signature = signatures[source].get(target.id)
            drum_signature = None if drum is None else signatures["Drums"].get(drum.id)
            if target_signature is None:
                failures.append(f"TARGET_SIGNATURE_{invalid_signature_reason[source][target.id]}")
            if drum is not None and drum_signature is None:
                failures.append(f"DRUM_SIGNATURE_{invalid_signature_reason['Drums'][drum.id]}")
            if target_signature is not None and drum_signature is not None:
                if target_signature != drum_signature:
                    failures.append("SIGNATURE_MISMATCH")
                else:
                    if len(signature_support[source][target_signature]) < 2:
                        failures.append("TARGET_SIGNATURE_NOT_RECURRENT")
                    if len(signature_support["Drums"][drum_signature]) < 2:
                        failures.append("DRUM_SIGNATURE_NOT_RECURRENT")
            record = {
                "contributor": source,
                "target": event_record(target, frames[target.id]),
                "drum": None if drum is None else event_record(drum, frames[drum.id]),
                "target_signature": target_signature,
                "drum_signature": drum_signature,
                "target_signature_recurrence": 0 if target_signature is None else len(signature_support[source][target_signature]),
                "drum_signature_recurrence": 0 if drum_signature is None else len(signature_support["Drums"][drum_signature]),
                "nearest_selection_status": localization.nearest_selection_status,
                "raw_geometric_displacement_seconds": localization.nearest_displacement_seconds,
                "status": "BLIND_CANDIDATE" if not failures else "UNRESOLVED",
                "failure_reasons": sorted(set(failures)),
            }
            (candidates if not failures else unresolved).append(record)

    content = {
        "schema": "H-VAL001-RHYTHM-CORRESPONDENCE-01-blind/v1",
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-01",
        "epistemic_status": "BLIND_FROZEN_NO_GROUND_TRUTH_ACCESS",
        "authority_checks": checks,
        "configuration": {"sample_rate": 44100, "hop_length": 512},
        "profile": {"profile_id": str(profile.profile_id), "scientific_fingerprint": profile.scientific_fingerprint},
        "population_counts": {name: len(events) for name, events in populations.items()},
        "frame_inventory": {
            name: [event_record(event, frames[event.id]) for event in events]
            for name, events in ordered.items()
        },
        "signature_inventory": {
            name: [{"eme_id": str(event.id), "signature": signatures[name].get(event.id),
                    "invalid_reason": invalid_signature_reason[name].get(event.id)} for event in events]
            for name, events in ordered.items()
        },
        "recurrence_inventory": {
            name: [{"signature": signature, "count": len(ids), "center_eme_ids": sorted(map(str, ids))}
                   for signature, ids in sorted(support.items())]
            for name, support in signature_support.items()
        },
        "candidates": sorted(candidates, key=lambda item: (item["contributor"], item["target"]["frame"], item["target"]["eme_id"])),
        "unresolved": sorted(unresolved, key=lambda item: (item["contributor"], item["target"]["frame"], item["target"]["eme_id"])),
    }
    content["summary"] = {
        "candidate_counts": dict(Counter(item["contributor"] for item in candidates)),
        "candidate_total": len(candidates),
        "unresolved_counts": dict(Counter(item["contributor"] for item in unresolved)),
        "unresolved_total": len(unresolved),
        "failure_reason_counts": dict(sorted(Counter(reason for item in unresolved for reason in item["failure_reasons"]).items())),
    }
    return content


def main():
    first = build_once()
    second = build_once()
    first_bytes, second_bytes = canonical(first), canonical(second)
    if first_bytes != second_bytes:
        raise RuntimeError("Deterministic blind replay failed")
    fingerprint = sha256(first_bytes).hexdigest()
    envelope = {
        "blind_scientific_fingerprint": fingerprint,
        "deterministic_replay": True,
        "scientific_content": first,
    }
    output = RUN / "blind_result.json"
    output.write_bytes(canonical(envelope) + b"\n")
    manifest = {
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-01",
        "phase": "BLIND_FROZEN",
        "blind_result_sha256": digest(output),
        "blind_scientific_fingerprint": fingerprint,
        "ground_truth_accessed": False,
        "deterministic_replay": True,
    }
    (RUN / "blind_manifest.json").write_bytes(canonical(manifest) + b"\n")
    print(json.dumps({**first["summary"], **manifest}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
