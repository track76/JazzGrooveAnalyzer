"""Score frozen raw system outputs against frozen symbolic GT."""
from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import sys

getcontext().prec = 50
BASE = Path("validation/CED-VAL-007-CONTROLLED-BEAT-BENCHMARK")
SCHEDULE = BASE / "symbolic_beat_reference.json"
SCHEDULE_SHA = "c2035145967dc436e08210d57a8ecdbe0ad39c309d253a06cb3c700a99405431"
WINDOW = Fraction(1, 8)
SAMPLE_RATE = 44100
INPUT_DURATION = Fraction(32, 1)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def checksum(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal(value: Fraction, places: int = 15) -> str:
    return f"{Decimal(value.numerator) / Decimal(value.denominator):.{places}f}"


def without_fingerprint(record: dict) -> dict:
    return {key: value for key, value in record.items() if key != "scientific_fingerprint"}


def linear_quantile(values: list[Fraction], p: Fraction) -> Fraction:
    ordered = sorted(values)
    position = Fraction(len(ordered) - 1) * p
    lower = position.numerator // position.denominator
    upper = lower if position.denominator == 1 else lower + 1
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def describe(values: list[Fraction]) -> dict:
    if not values:
        return {"count": 0, "statistics": "UNDEFINED"}
    fields = {
        "minimum": min(values),
        "q1_linear": linear_quantile(values, Fraction(1, 4)),
        "median_linear": linear_quantile(values, Fraction(1, 2)),
        "q3_linear": linear_quantile(values, Fraction(3, 4)),
        "maximum": max(values),
        "mean": sum(values, Fraction()) / len(values),
    }
    mean_decimal = sum(Decimal(value.numerator) / Decimal(value.denominator) for value in values) / Decimal(len(values))
    variance = sum((Decimal(value.numerator) / Decimal(value.denominator) - mean_decimal) ** 2 for value in values) / Decimal(len(values))
    sd = variance.sqrt()
    mean_square = sum((Decimal(value.numerator) / Decimal(value.denominator)) ** 2 for value in values) / Decimal(len(values))
    rmse = mean_square.sqrt()
    return {
        "count": len(values),
        "quartile_method": "linear_interpolation_at_(n-1)*p",
        "seconds": {name: {"exact": exact(value), "decimal": decimal(value)} for name, value in fields.items()} | {"population_standard_deviation": f"{sd:.15f}", "rmse": f"{rmse:.15f}"},
        "milliseconds": {name: {"exact": exact(value * 1000), "decimal": decimal(value * 1000)} for name, value in fields.items()} | {"population_standard_deviation": f"{sd * 1000:.15f}", "rmse": f"{rmse * 1000:.15f}"},
    }


def output_population(system: str, raw: dict) -> list[dict]:
    if sha256(canonical(without_fingerprint(raw))).hexdigest() != raw["scientific_fingerprint"]:
        raise RuntimeError(f"RAW_OUTPUT_FINGERPRINT_CONFLICT:{system}")
    source = raw["ad037_elementary_metric_events"] if system == "JGA" else raw["outputs"]
    result = []
    for index, item in enumerate(source):
        if system == "JGA":
            time = Fraction(item["producer_sample_coordinate"], SAMPLE_RATE)
            native_index = item["frozen_output_index"]
        elif system == "LIBROSA":
            time = Fraction(item["beat_sample"], SAMPLE_RATE)
            native_index = item["native_output_index"]
        else:
            time = Fraction.from_float(float.fromhex(item["beat_seconds_binary64_hex"]))
            native_index = item["native_output_index"]
        if time < 0:
            raise RuntimeError(f"NEGATIVE_SYSTEM_OUTPUT_AUTHORITY_CONFLICT:{system}:{index}")
        result.append({"output_id": item["output_id"], "native_output_index": native_index, "time": time})
    if any(result[i]["time"] > result[i + 1]["time"] for i in range(len(result) - 1)):
        raise RuntimeError(f"NONMONOTONIC_OUTPUT_AUTHORITY_CONFLICT:{system}")
    return result


def score(system: str, raw: dict, gt: list[dict]) -> dict:
    outputs = output_population(system, raw)
    unmatched = set(range(len(outputs)))
    matches = []
    misses = []
    for event in gt:
        candidates = []
        for index in sorted(unmatched):
            error = outputs[index]["time"] - event["time"]
            if abs(error) <= WINDOW:
                candidates.append((abs(error), outputs[index]["time"], outputs[index]["native_output_index"], index, error))
        if not candidates:
            misses.append({"gt_id": event["gt_id"], "gt_index": event["gt_index"], "gt_time_seconds_exact": exact(event["time"])})
            continue
        candidates.sort()
        chosen = candidates[0]
        same_distance = [candidate for candidate in candidates if candidate[0] == chosen[0]]
        index, error = chosen[3], chosen[4]
        unmatched.remove(index)
        matches.append({
            "gt_id": event["gt_id"],
            "gt_index": event["gt_index"],
            "gt_time_seconds_exact": exact(event["time"]),
            "system_output_id": outputs[index]["output_id"],
            "system_native_output_index": outputs[index]["native_output_index"],
            "system_time_seconds_exact": exact(outputs[index]["time"]),
            "signed_error_seconds_exact": exact(error),
            "absolute_error_seconds_exact": exact(abs(error)),
            "signed_error_milliseconds_decimal": decimal(error * 1000),
            "absolute_error_milliseconds_decimal": decimal(abs(error) * 1000),
            "signed_error_samples_exact": exact(error * SAMPLE_RATE),
            "tie": len(same_distance) > 1,
            "tied_candidate_output_ids": [outputs[candidate[3]]["output_id"] for candidate in same_distance],
            "tie_resolution": None if len(same_distance) == 1 else "EARLIER_TIMESTAMP_THEN_LOWER_NATIVE_OUTPUT_INDEX",
        })
    extras = [{
        "system_output_id": outputs[index]["output_id"],
        "system_native_output_index": outputs[index]["native_output_index"],
        "system_time_seconds_exact": exact(outputs[index]["time"]),
        "status": "OUTSIDE_INPUT_SCOPE_EXTRA" if outputs[index]["time"] >= INPUT_DURATION else "UNMATCHED_EXTRA",
    } for index in sorted(unmatched)]
    signed = [Fraction(item["signed_error_seconds_exact"]) for item in matches]
    absolute = [abs(value) for value in signed]
    matched = len(matches)
    raw_count = len(outputs)
    precision = Fraction(matched, raw_count) if raw_count else Fraction()
    recall = Fraction(matched, 64)
    f1 = Fraction(2) * precision * recall / (precision + recall) if precision + recall else Fraction()
    result = {
        "system": system,
        "gt_count": 64,
        "raw_output_count": raw_count,
        "matched_count": matched,
        "missed_gt_count": 64 - matched,
        "extra_output_count": raw_count - matched,
        "precision": {"exact": exact(precision), "decimal": decimal(precision)},
        "recall": {"exact": exact(recall), "decimal": decimal(recall)},
        "f1": {"exact": exact(f1), "decimal": decimal(f1)},
        "exact_zero_match_count": sum(value == 0 for value in signed),
        "signed_error_population_seconds_exact": [exact(value) for value in signed],
        "absolute_error_population_seconds_exact": [exact(value) for value in absolute],
        "signed_error_statistics": describe(signed),
        "absolute_error_statistics": describe(absolute),
        "matches": matches,
        "misses": misses,
        "extras": extras,
        "tie_count": sum(item["tie"] for item in matches),
        "raw_output_scientific_fingerprint": raw["scientific_fingerprint"],
        "assignment_rule": "ORDERED_DISJOINT_CLOSED_PLUS_MINUS_ONE_EIGHTH_SECOND_NEAREST_ONE_TO_ONE/v1",
    }
    if system in ("JGA", "LIBROSA"):
        sample_errors = [value * SAMPLE_RATE for value in signed]
        if any(value.denominator != 1 for value in sample_errors):
            raise RuntimeError(f"INTEGER_SAMPLE_ERROR_CONFLICT:{system}")
        result["signed_error_samples"] = [value.numerator for value in sample_errors]
        result["absolute_error_samples"] = [abs(value.numerator) for value in sample_errors]
    result["scientific_fingerprint"] = sha256(canonical(result)).hexdigest()
    return result


def main(raw_directory: Path, output_path: Path) -> None:
    authority = json.loads((raw_directory / "raw_system_output_authority.json").read_text())
    if authority["status"] != "FROZEN_BEFORE_GROUND_TRUTH_ACCESS" or authority["ground_truth_accessed_by_output_construction"]:
        raise RuntimeError("BLIND_FREEZE_AUTHORITY_CONFLICT")
    if checksum(SCHEDULE) != SCHEDULE_SHA:
        raise RuntimeError("GROUND_TRUTH_CHECKSUM_CONFLICT")
    schedule = json.loads(SCHEDULE.read_text())
    expected = [[i, 22050 * i, f"{i}/2" if i % 2 else f"{i // 2}/1"] for i in range(64)]
    if schedule["authority"] != "SYMBOLIC_BEAT_GROUND_TRUTH" or schedule["events"] != expected:
        raise RuntimeError("GROUND_TRUTH_AUTHORITY_CONFLICT")
    gt = [{"gt_id": f"GT-BEAT-{i:02d}", "gt_index": i, "time": Fraction(i, 2)} for i in range(64)]
    raw = {system: json.loads((raw_directory / filename).read_text()) for system, filename in {"JGA": "jga_raw_output.json", "LIBROSA": "librosa_raw_output.json", "ESSENTIA": "essentia_raw_output.json"}.items()}
    scores = {system: score(system, raw[system], gt) for system in ("JGA", "LIBROSA", "ESSENTIA")}
    combined_basis = {"ground_truth_sha256": SCHEDULE_SHA, "raw_output_authority_fingerprint": authority["combined_raw_output_fingerprint"], "system_score_fingerprints": {system: scores[system]["scientific_fingerprint"] for system in scores}}
    content = {
        "status": "PASS_COMMON_THREE_SYSTEM_SYMBOLIC_BEAT_RECOVERY_BENCHMARK",
        "ground_truth_authority": "SYMBOLIC_BEAT_GROUND_TRUTH",
        "ground_truth_count": 64,
        "raw_output_authority": authority,
        "systems": scores,
        "combined_benchmark_fingerprint_basis": combined_basis,
        "combined_benchmark_fingerprint": sha256(canonical(combined_basis)).hexdigest(),
        "algorithmic_dependency_caveat": "JGA uses librosa-based observation functionality and is not fully algorithmically independent from librosa beat_track; Essentia is the more independent comparator.",
        "jga_semantic_scope": "ability of the JGA Drums observational population to recover the controlled symbolic beat schedule",
        "claim_scope": "CED-VAL-007 controlled DS-Kick, 120 BPM, 4/4, 44.1 kHz, 64 quarter notes, 32-second render only",
        "firewalls": {"ground_truth_used_only_after_raw_output_freeze": True, "known_120_bpm_supplied": False, "marker_correction": False, "drum_latency_correction": False, "cedval004_latency_transfer": False, "h02_used": False, "strength_accessed": False, "production_code_changed": False, "raw_assets_changed": False, "historical_authorities_changed": False, "universal_superiority_claim": False},
    }
    output_path.write_text(json.dumps(content, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"combined_benchmark_fingerprint": content["combined_benchmark_fingerprint"], "counts": {system: {key: scores[system][key] for key in ("raw_output_count", "matched_count", "missed_gt_count", "extra_output_count")} for system in scores}, "status": content["status"]}, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: score.py RAW_DIRECTORY OUTPUT_PATH")
    main(Path(sys.argv[1]), Path(sys.argv[2]))
