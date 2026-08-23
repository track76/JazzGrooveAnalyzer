"""Execute frozen H-VAL001-CALIBRATION-PAIRWISE-01."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from statistics import fmean, median, pstdev

import numpy as np


BASE = Path("validation/VAL-001/run_20260823_095617")
ABS_BASE = Path("validation/VAL-001/run_20260823_070702")
PREREG = Path("validation/VAL-001/preregistrations/H-VAL001-CALIBRATION-PAIRWISE-01.md")
PAIR_AUTHORITY = BASE / "symbolic_pair_authority.json"
ABS_EVENTS = ABS_BASE / "event_level_results.json"
ABS_RESULT = ABS_BASE / "result.json"
ABS_INPUT_MANIFEST = ABS_BASE / "input_manifest.json"
SYMBOLIC_AUTHORITY = ABS_BASE / "calibration_symbolic_events.json"
INPUT_MANIFEST = BASE / "input_manifest.json"
EVENT_PAIRS = BASE / "event_pair_results.json"
RESULT = BASE / "result.json"
FRAME = Fraction(512, 44100)
SCOPE_END = Fraction(1865728, 44100)
SCOPE_MID = SCOPE_END / 2
RESAMPLES = 10_000
PAIR_SOURCES = ("Piano", "Double Bass", "Tenor Sax")
EXPECTED = {
    str(PREREG): "c5e066a46f6b6f8a46f6330aff5e5fb774f981f3ee38fbe0386bd95c48eacc06",
    str(SYMBOLIC_AUTHORITY): "038a970994dcb42961d115c6b5c7dd2a05c714b52f5fec3a1756133b5cdedd9f",
    str(ABS_EVENTS): "13fd9baa9510aa16acbec26547b2d732f0133f6090cda3fb5c1159b31d39c875",
    str(ABS_RESULT): "406f7ad0de0f95bf03272d0f058ab47d27b9f496e55b733453a026d7a9c61062",
    str(ABS_INPUT_MANIFEST): "71bc3439eddf781c6fed531d29e67340616ca3ab8352904dfa53b68e38c02600",
    "recordings/validation/ground_truth/03 THE COST OF LIVING versione intro + 8 bar.musicxml": "809a6ef276c4c3b9042c71d40a71763dcbf90d47e654e784af371eb53d073778",
    "recordings/validation/stems/drums.wav": "d09401036a750de70d8d7b14e4f508bc14f7b8ace2b0f629d6b707c00b33aafd",
    "recordings/validation/stems/piano.wav": "26fa1158f375598cc7c01e04379c00547ef1787f6862eb2f29a36aafd9007c7e",
    "recordings/validation/stems/double_bass.wav": "31d6f2e34d360c6f8f75362187433f2a2c1f5eb5cbbfe627305e99d07d8be6c5",
    "recordings/validation/stems/tenor_sax.wav": "89dd7e5c6063d3c4d5e4ac59c9119c265df4257dfb1b4a1e01b5f117ee87182e",
}


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def frac(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def fraction_record(value: Fraction) -> dict:
    return {
        "exact": f"{value.numerator}/{value.denominator}",
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": str(float(value)),
    }


def descriptive(values: tuple[float, ...]) -> dict:
    if not values:
        return {key: None for key in (
            "minimum", "maximum", "mean", "median",
            "population_standard_deviation", "q1", "q2", "q3"
        )} | {"n": 0}
    q1, q2, q3 = np.quantile(values, (0.25, 0.5, 0.75), method="linear")
    return {
        "n": len(values), "minimum": min(values), "maximum": max(values),
        "mean": fmean(values), "median": median(values),
        "population_standard_deviation": pstdev(values),
        "q1": float(q1), "q2": float(q2), "q3": float(q3),
    }


def seed_for(manifest_sha: str, label: str) -> int:
    return int(sha256(f"{manifest_sha}:{label}".encode()).hexdigest()[:16], 16)


def bootstrap(values: tuple[float, ...], manifest_sha: str, label: str) -> dict:
    if not values:
        return {"n": 0, "lower_95": None, "median": None, "upper_95": None}
    seed = seed_for(manifest_sha, label)
    rng = np.random.default_rng(seed)
    population = np.asarray(values, dtype=float)
    samples = rng.choice(population, (RESAMPLES, len(population)), replace=True)
    medians = np.median(samples, axis=1)
    low, high = np.quantile(medians, (0.025, 0.975), method="linear")
    return {
        "n": len(values), "lower_95": float(low), "median": median(values),
        "upper_95": float(high), "resamples": RESAMPLES, "seed": seed,
    }


def contains_zero(interval: dict) -> bool:
    return interval["lower_95"] <= 0 <= interval["upper_95"]


def excludes_zero(interval: dict) -> bool:
    return not contains_zero(interval)


def overlap(a: dict, b: dict) -> bool:
    return max(a["lower_95"], b["lower_95"]) <= min(a["upper_95"], b["upper_95"])


def sign(value: float) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def nearest_frame(error: Fraction) -> int:
    ratio = error / FRAME
    lower = ratio.numerator // ratio.denominator
    return min((lower, lower + 1), key=lambda k: (abs(ratio-k), abs(k), k))


def create_manifest(pair_sha: str, pair_fingerprint: str) -> str:
    absolute_manifest = json.loads(ABS_INPUT_MANIFEST.read_text())
    payload = {
        "experiment_id": "H-VAL001-CALIBRATION-PAIRWISE-01",
        "preregistration": {"path": str(PREREG), "sha256": EXPECTED[str(PREREG)]},
        "source_revision": "f7ce7927d1cad8f44fbfabcda4a40ba12de1c95b",
        "symbolic_pair_authority": {
            "path": str(PAIR_AUTHORITY), "sha256": pair_sha,
            "scientific_fingerprint": pair_fingerprint,
        },
        "frozen_inputs": EXPECTED,
        "absolute_calibration_environment": absolute_manifest["execution"],
        "observation": absolute_manifest["observation"],
        "sample_zero_relationship": absolute_manifest["authority"]["sample_zero_relationship"],
        "voice_status": "DEFERRED",
    }
    INPUT_MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return checksum(INPUT_MANIFEST)


def build_records(pair_authority: dict, absolute_events: dict) -> dict:
    absolute_by_source = {}
    for source, payload in absolute_events["correspondence_by_source"].items():
        absolute_by_source[source] = {
            record["calibration_symbolic_event_id"]: record
            for record in payload["event_results"]
        }
    output = {source: [] for source in PAIR_SOURCES}
    for pair in pair_authority["records"]:
        record = dict(pair)
        if pair["status"] != "VALID_SYMBOLIC_PAIR":
            record["jga_pair_status"] = pair["status"]
            output[pair["source"]].append(record)
            continue
        source_abs = absolute_by_source[pair["source"]][pair["source_symbolic_event_id"]]
        drum_abs = absolute_by_source["Drums"][pair["drum_symbolic_event_id"]]
        record["source_absolute_correspondence_status"] = source_abs["correspondence_status"]
        record["drum_absolute_correspondence_status"] = drum_abs["correspondence_status"]
        if source_abs["correspondence_status"] != "VALID" or drum_abs["correspondence_status"] != "VALID":
            record["jga_pair_status"] = "UNRESOLVED_JGA_PAIR"
            record["source_absolute_correspondence"] = source_abs
            record["drum_absolute_correspondence"] = drum_abs
            output[pair["source"]].append(record)
            continue
        source_gt = frac(source_abs["t_gt_seconds"])
        drum_gt = frac(drum_abs["t_gt_seconds"])
        source_jga = frac(source_abs["t_jga_seconds"])
        drum_jga = frac(drum_abs["t_jga_seconds"])
        delta_gt = source_gt - drum_gt
        delta_jga = source_jga - drum_jga
        error = delta_jga - delta_gt
        k = nearest_frame(error)
        residual = error - k * FRAME
        record.update({
            "jga_pair_status": "VALID_JGA_PAIR",
            "source_eme_id": source_abs["eme_id"], "drum_eme_id": drum_abs["eme_id"],
            "source_t_gt_seconds": source_abs["t_gt_seconds"], "drum_t_gt_seconds": drum_abs["t_gt_seconds"],
            "source_t_jga_seconds": source_abs["t_jga_seconds"], "drum_t_jga_seconds": drum_abs["t_jga_seconds"],
            "delta_gt_seconds": fraction_record(delta_gt), "delta_jga_seconds": fraction_record(delta_jga),
            "signed_e_pair_seconds": fraction_record(error), "absolute_e_pair_seconds": fraction_record(abs(error)),
            "signed_e_pair_ms": float(error * 1000), "absolute_e_pair_ms": float(abs(error) * 1000),
            "frame_offset": k, "frame_residual_seconds": fraction_record(residual),
            "frame_residual_ms": float(residual * 1000), "normalized_frame_residual": float(residual / FRAME),
            "adjacent_to_unmatched_or_ambiguous_cell": bool(source_abs["adjacent_to_unmatched_or_ambiguous_cell"] or drum_abs["adjacent_to_unmatched_or_ambiguous_cell"]),
            "source_asset_sha256": source_abs["source_asset_sha256"], "drum_asset_sha256": drum_abs["source_asset_sha256"],
            "source_supporting_pulse_candidate_ids": source_abs["supporting_pulse_candidate_ids"],
            "drum_supporting_pulse_candidate_ids": drum_abs["supporting_pulse_candidate_ids"],
            "source_contributor_id": source_abs["target_contributor_id"], "drum_contributor_id": drum_abs["target_contributor_id"],
            "source_sound_source_id": source_abs["target_sound_source_id"], "drum_sound_source_id": drum_abs["target_sound_source_id"],
            "materialization_rule": source_abs["materialization_rule"], "temporal_scope": source_abs["temporal_scope"],
        })
        output[pair["source"]].append(record)
    return output


def classify(records: list[dict], manifest_sha: str, source: str) -> dict:
    valid = [r for r in records if r["jga_pair_status"] == "VALID_JGA_PAIR"]
    first = [r for r in valid if frac(r["source_t_gt_seconds"]) < SCOPE_MID]
    second = [r for r in valid if frac(r["source_t_gt_seconds"]) >= SCOPE_MID]
    sensitivity = [r for r in valid if not r["adjacent_to_unmatched_or_ambiguous_cell"]]
    sens_first = [r for r in sensitivity if frac(r["source_t_gt_seconds"]) < SCOPE_MID]
    sens_second = [r for r in sensitivity if frac(r["source_t_gt_seconds"]) >= SCOPE_MID]
    groups = {"full": valid, "first_partition": first, "second_partition": second,
              "sensitivity_full": sensitivity, "sensitivity_first_partition": sens_first,
              "sensitivity_second_partition": sens_second}
    intervals = {name: bootstrap(tuple(r["signed_e_pair_ms"] for r in group), manifest_sha, f"{source}:{name}") for name, group in groups.items()}
    enough = len(valid) >= 10 and len(first) >= 5 and len(second) >= 5
    sens_enough = len(sensitivity) >= 10 and len(sens_first) >= 5 and len(sens_second) >= 5
    def candidate(prefix: str = "") -> bool:
        keys = [f"{prefix}full", f"{prefix}first_partition", f"{prefix}second_partition"]
        if any(intervals[k]["n"] == 0 for k in keys): return False
        medians = [intervals[k]["median"] for k in keys]
        return all(excludes_zero(intervals[k]) for k in keys) and len({sign(v) for v in medians}) == 1 and sign(medians[0]) != 0 and all(overlap(intervals[k], intervals[keys[0]]) for k in keys[1:])
    primary_candidate = enough and candidate()
    sensitivity_candidate = sens_enough and candidate("sensitivity_")
    primary_no = enough and contains_zero(intervals["full"]) and all(overlap(intervals[k], intervals["full"]) for k in ("first_partition", "second_partition"))
    sensitivity_no = sens_enough and contains_zero(intervals["sensitivity_full"]) and all(overlap(intervals[k], intervals["sensitivity_full"]) for k in ("sensitivity_first_partition", "sensitivity_second_partition"))
    if not enough or not sens_enough:
        outcome = "INSUFFICIENT_EVIDENCE"
    elif primary_candidate and sensitivity_candidate:
        outcome = "CANDIDATE_PAIRWISE_BIAS"
    elif primary_no and sensitivity_no:
        outcome = "NO_DETECTABLE_PAIRWISE_BIAS"
    else:
        outcome = "UNSTABLE_PAIRWISE_MEASUREMENT"
    signed = tuple(r["signed_e_pair_ms"] for r in valid)
    absolute = tuple(r["absolute_e_pair_ms"] for r in valid)
    return {
        "symbolic_pair_count": sum(r["status"] == "VALID_SYMBOLIC_PAIR" for r in records),
        "valid_jga_pair_count": len(valid),
        "unmatched_symbolic_pair_count": sum(r["status"] == "UNMATCHED_SYMBOLIC_PAIR" for r in records),
        "ambiguous_symbolic_pair_count": sum(r["status"] == "AMBIGUOUS_SYMBOLIC_PAIR" for r in records),
        "unresolved_jga_pair_count": sum(r["jga_pair_status"] == "UNRESOLVED_JGA_PAIR" for r in records),
        "signed_e_pair_ms": descriptive(signed), "absolute_e_pair_ms": descriptive(absolute),
        "bootstrap_intervals": intervals,
        "partition_counts": {"first": len(first), "second": len(second), "sensitivity_full": len(sensitivity), "sensitivity_first": len(sens_first), "sensitivity_second": len(sens_second)},
        "temporal_stability": outcome in ("CANDIDATE_PAIRWISE_BIAS", "NO_DETECTABLE_PAIRWISE_BIAS"),
        "classification": outcome,
        "frame_offsets": dict(sorted(Counter(r["frame_offset"] for r in valid).items())),
        "frame_residual_ms": descriptive(tuple(r["frame_residual_ms"] for r in valid)),
    }


def main() -> None:
    for path_text, expected in EXPECTED.items():
        if checksum(Path(path_text)) != expected:
            raise RuntimeError(f"Frozen checksum mismatch: {path_text}")
    pair_sha = checksum(PAIR_AUTHORITY)
    pair_authority = json.loads(PAIR_AUTHORITY.read_text())
    if pair_authority["authority_status"] != "FROZEN" or pair_authority["jga_timestamps_accessed"]:
        raise RuntimeError("Pair authority not independently frozen")
    manifest_sha = create_manifest(pair_sha, pair_authority["scientific_fingerprint"])
    absolute_events = json.loads(ABS_EVENTS.read_text())
    first_records = build_records(pair_authority, absolute_events)
    second_records = build_records(pair_authority, absolute_events)
    if first_records != second_records:
        raise RuntimeError("Event-pair deterministic replay mismatch")
    analyses = {source: classify(first_records[source], manifest_sha, source) for source in PAIR_SOURCES}
    replay_analyses = {source: classify(second_records[source], manifest_sha, source) for source in PAIR_SOURCES}
    if analyses != replay_analyses:
        raise RuntimeError("Analysis deterministic replay mismatch")
    event_payload = {
        "experiment_id": "H-VAL001-CALIBRATION-PAIRWISE-01",
        "input_manifest_sha256": manifest_sha,
        "symbolic_pair_authority_sha256": pair_sha,
        "records_by_source": first_records,
    }
    EVENT_PAIRS.write_text(json.dumps(event_payload, indent=2, sort_keys=True) + "\n")
    outcomes = {source: analyses[source]["classification"] for source in PAIR_SOURCES}
    overall = next(iter(set(outcomes.values()))) if len(set(outcomes.values())) == 1 else "MIXED_SOURCE_SPECIFIC_OUTCOME"
    cancellation = {source: ("YES" if outcome == "NO_DETECTABLE_PAIRWISE_BIAS" else "NO" if outcome == "CANDIDATE_PAIRWISE_BIAS" else "PARTIAL") for source, outcome in outcomes.items()}
    frame_offsets = Counter()
    residuals = []
    for source in PAIR_SOURCES:
        for record in first_records[source]:
            if record["jga_pair_status"] == "VALID_JGA_PAIR":
                frame_offsets[record["frame_offset"]] += 1
                residuals.append(record["frame_residual_ms"])
    scientific_content = {
        "experiment_id": "H-VAL001-CALIBRATION-PAIRWISE-01",
        "symbolic_pair_authority_fingerprint": pair_authority["scientific_fingerprint"],
        "records_by_source": first_records, "analyses": analyses,
        "overall_classification": overall, "common_absolute_bias_cancellation": cancellation,
        "frame_offsets": dict(sorted(frame_offsets.items())), "frame_residual_ms": descriptive(tuple(residuals)),
    }
    # Canonicalize JSON object keys before fingerprinting so independent
    # replay from the serialized artifact reproduces the same content.
    scientific_content = json.loads(json.dumps(scientific_content))
    fingerprint = sha256(json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    result = {
        **scientific_content, "scientific_fingerprint": fingerprint,
        "deterministic_replay": True, "bootstrap_status": "PASS",
        "raw_observations_modified": False, "correction_authorized": False,
        "geometric_nearest_drum_matching_used": False, "correspondence_tolerance_used": False,
        "voice_status": "DEFERRED", "input_manifest_sha256": manifest_sha,
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("STATUS=PASS")
    print(f"SCIENTIFIC_FINGERPRINT={fingerprint}")
    print(json.dumps({s: analyses[s] for s in PAIR_SOURCES}, sort_keys=True))


if __name__ == "__main__":
    main()
