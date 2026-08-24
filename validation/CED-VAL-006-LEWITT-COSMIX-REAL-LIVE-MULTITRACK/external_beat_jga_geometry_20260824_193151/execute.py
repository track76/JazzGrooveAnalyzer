"""Execute the frozen external-beat-to-JGA-Drums geometry protocol."""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path

BASE = Path("validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK")
JGA_RUN = BASE / "run_20260824_183919"
TRACKER_RUN = BASE / "external_beat_benchmark_20260824_191341"
RUN = BASE / "external_beat_jga_geometry_20260824_193151"
PREREG = BASE / "preregistrations/H-CEDVAL006-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01.md"
STUDY_ID = "H-CEDVAL006-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY-01"
EXECUTION_ID = "EXEC-CEDVAL006-EXTERNAL-BEAT-JGA-GEOMETRY-20260824-193151"
JGA_EXECUTION_ID = "EXEC-CEDVAL006-REAL-LIVE-AUDIO-20260824-183919"
JGA_FINGERPRINT = "8c5723fbeabe2031516b2eeee0c83fb42ad84f46824cf65f5d485c6cf6c82b5c"
TRACKER_EXECUTION_ID = "EXEC-CEDVAL006-EXTERNAL-BEAT-BENCHMARK-20260824-191341"
TRACKER_FINGERPRINT = "d3e5ea9c6bea7bd0a9c81cb6044fa469dc1f33bc2f70788cd4a027f30491ee6a"
ESSENTIA_FINGERPRINT = "1e52e479e9be6bb80f7b36a781031ab343523c4e6d7d248eecfaf4cb9bd284dd"
LIBROSA_FINGERPRINT = "780f9691dd13bb7bf30858ff8a7d76628958f42b8e56430798554981ef65b318"
SR, HOP = 48000, 512
INPUT_HASHES = {
    "jga_eme": "64db95d8feeb6ab7ca22aa8081e177c57d6ab57c9f0aaf3bb4a5650db28329f5",
    "essentia": "3f3ff0e855b646c29ee56e775c3d2a20a0cf37468242137e3406dc9203cb9b45",
    "librosa": "8ff07eb46d7f8c734d64c37874e595d1c4172cab1a9d66d03b930bf3cec6dea0",
    "preregistration": "df54e09ac64f9611248f5b2de1f4d7208ef03ab8e149540c4f78b069c056cc72",
}
PATHS = {
    "jga_eme": JGA_RUN / "elementary_metric_events.json",
    "essentia": TRACKER_RUN / "essentia_output.json",
    "librosa": TRACKER_RUN / "librosa_output.json",
    "preregistration": PREREG,
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def rational(value: Fraction) -> dict:
    rendered = float(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "seconds_binary64": rendered,
        "seconds_binary64_hex": rendered.hex(),
        "milliseconds_binary64": rendered * 1000.0,
    }


def statistic(value: Fraction) -> dict:
    rendered = float(value)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "seconds_binary64": rendered,
        "seconds_binary64_hex": rendered.hex(),
        "milliseconds_binary64": rendered * 1000.0,
    }


def quantile(values: list[Fraction], p: Fraction) -> Fraction:
    ordered = sorted(values)
    position = Fraction(len(ordered) - 1) * p
    lower = position.numerator // position.denominator
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def stats(values: list[Fraction]) -> dict:
    mean = sum(values, Fraction()) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    sd = math.sqrt(float(variance))
    return {
        "count": len(values),
        "minimum": statistic(min(values)),
        "q1_linear": statistic(quantile(values, Fraction(1, 4))),
        "median_linear": statistic(quantile(values, Fraction(1, 2))),
        "q3_linear": statistic(quantile(values, Fraction(3, 4))),
        "maximum": statistic(max(values)),
        "mean": statistic(mean),
        "population_variance": {"numerator": variance.numerator, "denominator": variance.denominator},
        "population_sd_seconds_binary64": sd,
        "population_sd_seconds_binary64_hex": sd.hex(),
        "population_sd_milliseconds_binary64": sd * 1000.0,
    }


def verify_authorities() -> tuple[list[dict], dict, dict]:
    for identity, expected in INPUT_HASHES.items():
        observed = checksum(PATHS[identity])
        if observed != expected:
            raise RuntimeError(f"EVIDENCE_CONFLICT_CHECKSUM: {identity}: {observed}")
    jga_manifest = json.loads((JGA_RUN / "artifact_manifest.json").read_text())
    tracker_result = json.loads((TRACKER_RUN / "result.json").read_text())
    if (jga_manifest.get("execution_id"), jga_manifest.get("scientific_fingerprint")) != (JGA_EXECUTION_ID, JGA_FINGERPRINT):
        raise RuntimeError("EVIDENCE_CONFLICT_JGA_AUTHORITY")
    if (tracker_result.get("execution_id"), tracker_result.get("combined_benchmark_fingerprint")) != (TRACKER_EXECUTION_ID, TRACKER_FINGERPRINT):
        raise RuntimeError("EVIDENCE_CONFLICT_TRACKER_AUTHORITY")
    events = json.loads(PATHS["jga_eme"].read_text())
    drums = events.get("Drums", [])
    essentia = json.loads(PATHS["essentia"].read_text())
    librosa = json.loads(PATHS["librosa"].read_text())
    if essentia.get("scientific_fingerprint") != ESSENTIA_FINGERPRINT:
        raise RuntimeError("EVIDENCE_CONFLICT_ESSENTIA_AUTHORITY")
    if librosa.get("scientific_fingerprint") != LIBROSA_FINGERPRINT:
        raise RuntimeError("EVIDENCE_CONFLICT_LIBROSA_AUTHORITY")
    if len(drums) != 909 or len(essentia["native_outputs"]["ticks"]["seconds"]) != 527 or len(librosa["native_outputs"]["beat_frames"]["values"]) != 466:
        raise RuntimeError("EVIDENCE_CONFLICT_POPULATION_CARDINALITY")
    for event in drums:
        sample = event["producer_sample_coordinate"]
        if sample != HOP * event["producer_frame"]:
            raise RuntimeError(f"EVIDENCE_CONFLICT_JGA_SAMPLE: {event['eme_id']}")
        timestamp = sample / SR
        if timestamp != event["timestamp_seconds"] or timestamp.hex() != event["timestamp_hex"]:
            raise RuntimeError(f"EVIDENCE_CONFLICT_JGA_TIMESTAMP: {event['eme_id']}")
    return drums, essentia, librosa


def drum_authority(drums: list[dict]) -> tuple[list[Fraction], dict[Fraction, list[dict]]]:
    groups: dict[Fraction, list[dict]] = {}
    for event in drums:
        time = Fraction(event["producer_sample_coordinate"], SR)
        groups.setdefault(time, []).append(event)
    for events in groups.values():
        events.sort(key=lambda item: item["eme_id"])
    return sorted(groups), groups


def identity_record(event: dict) -> dict:
    return {
        "eme_id": event["eme_id"],
        "producer_frame": event["producer_frame"],
        "producer_sample_coordinate": event["producer_sample_coordinate"],
        "timestamp_seconds": event["timestamp_seconds"],
        "timestamp_hex": event["timestamp_hex"],
    }


def external_populations(essentia: dict, librosa: dict) -> dict[str, list[dict]]:
    essentia_beats = []
    for index, item in enumerate(essentia["native_outputs"]["ticks"]["seconds"]):
        value = float.fromhex(item["binary64_hex"])
        if value != item["decimal"]:
            raise RuntimeError(f"EVIDENCE_CONFLICT_ESSENTIA_BINARY64: {index}")
        time = Fraction(*value.as_integer_ratio())
        essentia_beats.append({
            "external_beat_id": f"ESSENTIA-TICK-{index:04d}",
            "native_index": index,
            "timestamp_seconds": value,
            "timestamp_hex": value.hex(),
            "time": time,
        })
    frames = librosa["native_outputs"]["beat_frames"]["values"]
    samples = librosa["native_outputs"]["beat_samples"]["values"]
    seconds = librosa["native_outputs"]["beat_seconds"]["values"]
    librosa_beats = []
    for index, (frame, sample, item) in enumerate(zip(frames, samples, seconds, strict=True)):
        if sample != HOP * frame:
            raise RuntimeError(f"EVIDENCE_CONFLICT_LIBROSA_SAMPLE: {index}")
        rendered = sample / SR
        if rendered != item["decimal"] or rendered.hex() != item["binary64_hex"]:
            raise RuntimeError(f"EVIDENCE_CONFLICT_LIBROSA_TIMESTAMP: {index}")
        librosa_beats.append({
            "external_beat_id": f"LIBROSA-BEAT-{index:04d}",
            "native_index": index,
            "beat_frame": frame,
            "beat_sample": sample,
            "timestamp_seconds": rendered,
            "timestamp_hex": rendered.hex(),
            "time": Fraction(sample, SR),
        })
    return {"Essentia": essentia_beats, "librosa": librosa_beats}


def analyze_tracker(tracker: str, beats: list[dict], drum_times: list[Fraction], groups: dict[Fraction, list[dict]]) -> dict:
    cases = []
    signed_population: list[Fraction] = []
    absolute_population: list[Fraction] = []
    availability = {"preceding": 0, "following": 0, "nearest": 0}
    tie_count = 0
    boundary_counts = {"BEFORE_FIRST_JGA_OBSERVATION": 0, "AFTER_LAST_JGA_OBSERVATION": 0, "INTERIOR_OR_ENDPOINT": 0}
    for beat in beats:
        b = beat["time"]
        preceding_index = bisect_right(drum_times, b) - 1
        following_index = bisect_right(drum_times, b)
        preceding_time = drum_times[preceding_index] if preceding_index >= 0 else None
        following_time = drum_times[following_index] if following_index < len(drum_times) else None
        candidate_times = [time for time in (preceding_time, following_time) if time is not None]
        if not candidate_times:
            raise RuntimeError("UNRESOLVED_EMPTY_DRUM_AUTHORITY")
        nearest_distance = min(abs(time - b) for time in candidate_times)
        nearest_times = [time for time in candidate_times if abs(time - b) == nearest_distance]
        nearest_events = [event for time in nearest_times for event in groups[time]]
        ranked = sorted(nearest_events, key=lambda event: (
            0 if Fraction(event["producer_sample_coordinate"], SR) <= b else 1,
            Fraction(event["producer_sample_coordinate"], SR), event["eme_id"],
        ))
        representative = ranked[0]
        representative_time = Fraction(representative["producer_sample_coordinate"], SR)
        signed = representative_time - b
        absolute = abs(signed)
        signed_population.append(signed)
        absolute_population.append(absolute)
        availability["nearest"] += 1
        if preceding_time is not None:
            availability["preceding"] += 1
        if following_time is not None:
            availability["following"] += 1
        tied = len(nearest_events) > 1
        tie_count += int(tied)
        if b < drum_times[0]:
            boundary = "BEFORE_FIRST_JGA_OBSERVATION"
        elif b > drum_times[-1]:
            boundary = "AFTER_LAST_JGA_OBSERVATION"
        else:
            boundary = "INTERIOR_OR_ENDPOINT"
        boundary_counts[boundary] += 1
        external = {key: value for key, value in beat.items() if key != "time"}
        external["exact_time"] = rational(b)
        cases.append({
            "external_beat": external,
            "preceding_jga_drums": [] if preceding_time is None else [identity_record(event) for event in groups[preceding_time]],
            "following_jga_drums": [] if following_time is None else [identity_record(event) for event in groups[following_time]],
            "nearest_jga_drums": [identity_record(event) for event in nearest_events],
            "serialization_representative_eme_id": representative["eme_id"],
            "nearest_status": "EQUAL_DISTANCE_TIE" if tied else "UNIQUE_NEAREST",
            "boundary_status": boundary,
            "signed_displacement": rational(signed),
            "absolute_displacement": rational(absolute),
        })
    frame = Fraction(HOP, SR)
    exact_zero = sum(value == 0 for value in absolute_population)
    within_one = sum(value <= frame for value in absolute_population)
    within_two = sum(value <= 2 * frame for value in absolute_population)
    beyond_two = sum(value > 2 * frame for value in absolute_population)
    disjoint = {
        "equal_zero": exact_zero,
        "greater_zero_through_one_frame": sum(0 < value <= frame for value in absolute_population),
        "greater_one_through_two_frames": sum(frame < value <= 2 * frame for value in absolute_population),
        "greater_two_frames": beyond_two,
    }
    summary = {
        "external_beat_count": len(beats),
        "localized_count": len(cases),
        "unresolved_count": 0,
        "availability_counts": availability,
        "tie_count": tie_count,
        "boundary_status_counts": boundary_counts,
        "signed_displacement_statistics": stats(signed_population),
        "absolute_displacement_statistics": stats(absolute_population),
        "frame_lattice_descriptive_counts": {
            "exact_zero_count": exact_zero,
            "within_one_jga_frame_count": within_one,
            "within_two_jga_frames_count": within_two,
            "beyond_two_jga_frames_count": beyond_two,
            "disjoint_audit_bins": disjoint,
            "jga_frame_duration": rational(frame),
            "epistemic_status": "DESCRIPTIVE_COUNTS_NOT_THRESHOLDS_OR_TOLERANCES",
        },
    }
    content = {
        "tracker": tracker,
        "epistemic_status": "CANDIDATE_EXTERNAL_TEMPORAL_REFERENCE",
        "jga_epistemic_status": "FRAME-RESOLVED OBSERVATION",
        "relation_status": "DESCRIPTIVE_TEMPORAL_GEOMETRY_ONLY",
        "cases": cases,
        "signed_displacement_population": [rational(value) for value in signed_population],
        "absolute_displacement_population": [rational(value) for value in absolute_population],
        "summary": summary,
    }
    content["scientific_fingerprint"] = sha256(canonical(content)).hexdigest()
    return content


def derive() -> dict:
    drums, essentia, librosa = verify_authorities()
    drum_times, groups = drum_authority(drums)
    populations = external_populations(essentia, librosa)
    analyses = {
        tracker: analyze_tracker(tracker, beats, drum_times, groups)
        for tracker, beats in populations.items()
    }
    content = {
        "schema": "JGA-CEDVAL006-EXTERNAL-BEAT-TO-JGA-DRUMS-GEOMETRY/v1",
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "preregistration_commit": "51ce4fe9ad01db14229fad658170ae1d94e824d8",
        "authorities": {
            "jga_execution_id": JGA_EXECUTION_ID,
            "jga_scientific_fingerprint": JGA_FINGERPRINT,
            "jga_drums_eme_count": 909,
            "external_execution_id": TRACKER_EXECUTION_ID,
            "external_combined_fingerprint": TRACKER_FINGERPRINT,
            "essentia_scientific_fingerprint": ESSENTIA_FINGERPRINT,
            "essentia_beat_count": 527,
            "librosa_scientific_fingerprint": LIBROSA_FINGERPRINT,
            "librosa_beat_count": 466,
            "input_sha256": INPUT_HASHES,
        },
        "coordinate_authority": "EXACT_ELAPSED_DISTRIBUTED_FILE_TIME_FROM_SAMPLE_ZERO",
        "algorithmic_dependency_caveat": {
            "librosa_and_jga_frontend_fully_independent": False,
            "frozen_equal_start_seconds": 26.528,
            "essentia_more_algorithmically_independent_comparator": True,
            "geometry_rule_changed_by_dependency": False,
            "epistemic_effect": "LIBROSA_ALIGNMENT_CANNOT_INDEPENDENTLY_VALIDATE_JGA",
        },
        "analyses": analyses,
        "scope_policy": {
            "complete_frozen_populations_analyzed": True,
            "tracker_populations_trimmed": False,
            "boundary_cases_preserved": True,
            "secondary_common_overlap_statistics": "NOT_PREREGISTERED",
        },
        "future_five_window_visualization_only": [
            ["W1", 1071286, 1311286], ["W2", 3453860, 3693860],
            ["W3", 5836434, 6076434], ["W4", 8219007, 8459007],
            ["W5", 10601581, 10841581],
        ],
        "firewalls": {
            "ground_truth_created": False,
            "musical_interpretation_performed": False,
            "tracker_to_tracker_correspondence_performed": False,
            "tracker_to_tracker_comparison_performed": False,
            "preferred_tracker_selected": False,
            "beat_validation_claimed": False,
            "bpm_used_as_comparison_input": False,
            "h02_used": False,
            "strength_accessed": False,
            "jga_rerun": False,
            "external_trackers_rerun": False,
            "jga_core_changed": False,
            "production_code_changed": False,
            "historical_authorities_changed": False,
            "visualization_rendered": False,
        },
    }
    fingerprint_basis = {key: value for key, value in content.items() if key != "combined_comparison_fingerprint"}
    content["combined_comparison_fingerprint"] = sha256(canonical(fingerprint_basis)).hexdigest()
    return content


def freeze(pass_one: Path, pass_two: Path) -> None:
    first_bytes = pass_one.read_bytes()
    second_bytes = pass_two.read_bytes()
    if first_bytes != second_bytes:
        raise RuntimeError("DETERMINISTIC_REPLAY_FAILURE")
    first = json.loads(first_bytes)
    if first != derive():
        raise RuntimeError("FREEZE_DERIVATION_CONFLICT")
    RUN.mkdir(parents=True, exist_ok=True)
    write_json(RUN / "scientific_content.json", first)
    result = {
        "status": "PASS_FROZEN_NEUTRAL_EXTERNAL_BEAT_TO_JGA_DRUMS_GEOMETRY",
        "execution_id": EXECUTION_ID,
        "study_id": STUDY_ID,
        "combined_comparison_fingerprint": first["combined_comparison_fingerprint"],
        "essentia_scientific_fingerprint": first["analyses"]["Essentia"]["scientific_fingerprint"],
        "librosa_scientific_fingerprint": first["analyses"]["librosa"]["scientific_fingerprint"],
        "deterministic_replay": "PASS_EXACT_TWO_FRESH_PROCESS_EXECUTIONS",
        "summaries": {name: analysis["summary"] for name, analysis in first["analyses"].items()},
        "firewalls": first["firewalls"],
    }
    write_json(RUN / "result.json", result)
    write_json(RUN / "input_manifest.json", {
        "authority_gate": "PASS",
        "authorities": first["authorities"],
        "preregistration_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
    })
    write_json(RUN / "completion_protocol.json", {
        "status": result["status"],
        "deterministic_replay": result["deterministic_replay"],
        "combined_comparison_fingerprint": result["combined_comparison_fingerprint"],
        "epistemic_status": "DESCRIPTIVE_TEMPORAL_GEOMETRY_ONLY",
        "firewalls": first["firewalls"],
    })
    report = [
        f"# {STUDY_ID} Frozen Result", "", f"Execution: `{EXECUTION_ID}`", "",
        f"Scientific fingerprint: `{result['combined_comparison_fingerprint']}`", "",
        "Status: **PASS_FROZEN_NEUTRAL_EXTERNAL_BEAT_TO_JGA_DRUMS_GEOMETRY**", "",
        "The two frozen external beat populations were independently localized against the frozen 909-event JGA Drums EME population using exact distributed-file-time geometry. Two fresh-process derivations reproduced byte-identical scientific content.", "",
        "The librosa tracker and JGA observation frontend are not fully algorithmically independent; librosa alignment cannot independently validate JGA. Essentia is the more algorithmically independent comparator. This caveat did not alter the geometry.", "",
        "The result is descriptive temporal geometry only. It establishes no Ground Truth, BeatReference authority, event correspondence, detector accuracy, synchronization, physical onset, human microtiming, tracker preference, or musical interpretation.",
    ]
    (RUN / "report.md").write_text("\n".join(report) + "\n")
    artifacts = ["execute.py", "verify.py", "input_manifest.json", "scientific_content.json", "result.json", "completion_protocol.json", "report.md"]
    write_json(RUN / "artifact_manifest.json", {
        "study_id": STUDY_ID,
        "execution_id": EXECUTION_ID,
        "combined_comparison_fingerprint": result["combined_comparison_fingerprint"],
        "artifacts": {name: checksum(RUN / name) for name in artifacts},
    })
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    derive_parser = subparsers.add_parser("derive")
    derive_parser.add_argument("output", type=Path)
    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("pass_one", type=Path)
    freeze_parser.add_argument("pass_two", type=Path)
    args = parser.parse_args()
    if args.command == "derive":
        write_json(args.output, derive())
    else:
        freeze(args.pass_one, args.pass_two)


if __name__ == "__main__":
    main()
