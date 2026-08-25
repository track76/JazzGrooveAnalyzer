#!/usr/bin/env python3
"""Frozen CED-VAL-006 controlled-mix separation robustness scorer."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics


HERE = Path(__file__).resolve().parent
DATASET = HERE.parent
REFERENCE = DATASET / "acceptance_20260825_113950/canonical_report_execution_1.json"
REPORTS = {
    "run_1": HERE / "canonical_report_run_1.json",
    "run_2": HERE / "canonical_report_run_2.json",
}
SCOPE_END = Fraction(11912868, 48000)


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "seconds": float(value),
        "seconds_hex": float(value).hex(),
    }


def quantile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def stats(values: list[float]) -> dict[str, object]:
    if not values:
        return {key: None for key in (
            "count", "minimum", "q1_linear", "median", "q3_linear",
            "maximum", "mean", "population_sd", "rmse",
        )}
    return {
        "count": len(values),
        "minimum": min(values),
        "q1_linear": quantile(values, 0.25),
        "median": quantile(values, 0.5),
        "q3_linear": quantile(values, 0.75),
        "maximum": max(values),
        "mean": statistics.fmean(values),
        "population_sd": statistics.pstdev(values),
        "rmse": math.sqrt(statistics.fmean(value * value for value in values)),
    }


def events(report: dict[str, object], label: str) -> list[dict[str, object]]:
    authority = next(item for item in report["source_authorities"] if item["label"] == label)
    sample_rate = authority["technical_audio"]["sample_rate_hz"]
    observations = {item["pulse_candidate_id"]: item for item in report["observations"][label]}
    source_sha = authority["sha256"]
    selected = []
    for eme in report["elementary_metric_events"]:
        if eme["source_asset_sha256"] != source_sha:
            continue
        observation = observations[eme["supporting_pulse_candidate_ids"][0]]
        coordinate = Fraction(observation["producer_sample_coordinate"], sample_rate)
        selected.append({
            "eme_id": eme["eme_id"],
            "native_index": observation["observation_index"],
            "producer_sample_coordinate": observation["producer_sample_coordinate"],
            "sample_rate_hz": sample_rate,
            "time": coordinate,
        })
    return sorted(selected, key=lambda item: (item["time"], item["native_index"]))


def assign(original: list[dict[str, object]], separated: list[dict[str, object]]) -> dict[str, object]:
    used: set[str] = set()
    matches = []
    original_only = []
    for index, event in enumerate(original):
        left = Fraction(0) if index == 0 else (original[index - 1]["time"] + event["time"]) / 2
        right = SCOPE_END if index == len(original) - 1 else (event["time"] + original[index + 1]["time"]) / 2
        candidates = [item for item in separated if item["eme_id"] not in used and left <= item["time"] < right]
        candidates.sort(key=lambda item: (abs(item["time"] - event["time"]), item["time"], item["native_index"]))
        if not candidates:
            original_only.append({
                "original_eme_id": event["eme_id"],
                "original_time": fraction_record(event["time"]),
                "cell_left": fraction_record(left),
                "cell_right": fraction_record(right),
            })
            continue
        chosen = candidates[0]
        used.add(chosen["eme_id"])
        displacement = chosen["time"] - event["time"]
        tied = [item["eme_id"] for item in candidates
                if abs(item["time"] - event["time"]) == abs(displacement)]
        matches.append({
            "original_eme_id": event["eme_id"],
            "separated_eme_id": chosen["eme_id"],
            "original_time": fraction_record(event["time"]),
            "separated_time": fraction_record(chosen["time"]),
            "signed_displacement": fraction_record(displacement),
            "absolute_displacement": fraction_record(abs(displacement)),
            "cell_left": fraction_record(left),
            "cell_right": fraction_record(right),
            "minimum_displacement_tied_separated_ids": tied,
            "selection_reason": "MIN_ABSOLUTE_THEN_EARLIER_TIME_THEN_NATIVE_INDEX",
        })
    separated_only = [{
        "separated_eme_id": item["eme_id"],
        "separated_time": fraction_record(item["time"]),
        "outside_original_scope": not (Fraction(0) <= item["time"] < SCOPE_END),
    } for item in separated if item["eme_id"] not in used]
    signed = [item["signed_displacement"]["seconds"] for item in matches]
    absolute = [item["absolute_displacement"]["seconds"] for item in matches]
    precision = len(matches) / len(separated) if separated else 0.0
    recall = len(matches) / len(original) if original else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "raw_original_count": len(original),
        "raw_separated_count": len(separated),
        "matched_count": len(matches),
        "original_only_count": len(original_only),
        "separated_only_count": len(separated_only),
        "descriptive_precision": precision,
        "descriptive_recall": recall,
        "descriptive_f1": f1,
        "exact_zero_count": sum(value == 0.0 for value in signed),
        "signed_displacement_statistics": stats(signed),
        "absolute_displacement_statistics": stats(absolute),
        "matches": matches,
        "original_only": original_only,
        "separated_only": separated_only,
        "scientific_status": "CROSS_CONDITION_TEMPORAL_STABILITY_ONLY_NOT_PHYSICAL_ONSET_ERROR",
    }


def level1(original: list[dict[str, object]], separated: list[dict[str, object]], scope: Fraction) -> dict[str, object]:
    difference = len(separated) - len(original)
    def coverage(population: list[dict[str, object]]) -> dict[str, object]:
        first = population[0]["time"] if population else None
        last = population[-1]["time"] if population else None
        return {
            "first_eme_time": fraction_record(first) if first is not None else None,
            "last_eme_time": fraction_record(last) if last is not None else None,
            "eme_temporal_span": fraction_record(last - first) if first is not None else None,
        }
    return {
        "original_eme_count": len(original),
        "separated_eme_count": len(separated),
        "signed_count_difference": difference,
        "absolute_count_difference": abs(difference),
        "relative_count_difference": difference / len(original),
        "original_temporal_coverage": coverage(original),
        "separated_temporal_coverage": coverage(separated),
        "scope_duration": fraction_record(scope),
        "original_event_density_per_second": len(original) / float(scope),
        "separated_event_density_per_second": len(separated) / float(scope),
        "count_equality_is_event_identity": False,
    }


def level3(reference: dict[str, object], separated: dict[str, object], mappings: dict[str, dict[str, object]]) -> dict[str, object]:
    original_locs = {item["target_eme_id"]: item for item in reference["ad038_localizations"]}
    separated_locs = {item["target_eme_id"]: item for item in separated["ad038_localizations"]}
    bass_map = {item["original_eme_id"]: item["separated_eme_id"] for item in mappings["Double Bass"]["matches"]}
    drum_map = {item["original_eme_id"]: item["separated_eme_id"] for item in mappings["Drums"]["matches"]}
    relation_records = []
    identity_counts = {name: {"stable": 0, "scorable": 0} for name in ("nearest", "predecessor", "follower")}
    paired = []
    for original_bass, separated_bass in sorted(bass_map.items()):
        old = original_locs[original_bass]
        new = separated_locs[separated_bass]
        record = {"original_target_eme_id": original_bass, "separated_target_eme_id": separated_bass}
        all_scorable = True
        for name, field in (("nearest", "nearest_reference"), ("predecessor", "preceding_reference"), ("follower", "following_reference")):
            old_ref = old[field]
            new_ref = new[field]
            if old_ref is None:
                scorable = new_ref is None
                mapped = None
                stable = scorable
            else:
                mapped = drum_map.get(old_ref["eme_id"])
                scorable = mapped is not None
                stable = scorable and new_ref is not None and new_ref["eme_id"] == mapped
            if scorable:
                identity_counts[name]["scorable"] += 1
                identity_counts[name]["stable"] += int(stable)
            else:
                all_scorable = False
            record[name] = {
                "original_reference_eme_id": old_ref["eme_id"] if old_ref else None,
                "mapped_separated_reference_eme_id": mapped,
                "observed_separated_reference_eme_id": new_ref["eme_id"] if new_ref else None,
                "status": "STABLE" if stable else ("DIFFERENT" if scorable else "UNSCORABLE_UNMATCHED_REFERENCE"),
            }
        difference = new["nearest_displacement_seconds"] - old["nearest_displacement_seconds"]
        record["nearest_displacement_difference_seconds"] = difference
        record["nearest_displacement_difference_hex"] = difference.hex()
        paired.append(difference)
        record["all_required_references_scorable"] = all_scorable
        relation_records.append(record)
    for value in identity_counts.values():
        value["rate"] = value["stable"] / value["scorable"] if value["scorable"] else None
    def geometry(report: dict[str, object]) -> dict[str, object]:
        locs = report["ad038_localizations"]
        signed = [item["nearest_displacement_seconds"] for item in locs]
        absolute = [item["nearest_absolute_displacement_seconds"] for item in locs]
        return {
            "eligible": len(report["elementary_metric_events"]) - next(item["eme_count"] for item in report["source_authorities"] if item["role"] == "TEMPORAL_REFERENCE"),
            "localized": len(locs),
            "unresolved": sum(item["nearest_reference"] is None for item in locs),
            "ties": sum(item["nearest_selection_status"] != "UNIQUE" for item in locs),
            "signed_nearest_displacement_population": signed,
            "absolute_nearest_displacement_population": absolute,
            "signed_statistics": stats(signed),
            "absolute_statistics": stats(absolute),
        }
    old_profile = reference["ad040_profile"]
    new_profile = separated["ad040_profile"]
    profile_fields = (
        "temporal_reference_eme_count", "accompaniment_relationship_count",
        "represented_eme_count", "temporal_origin_seconds", "temporal_scope",
        "projection_rule", "calibration_status", "correspondence_status_counts",
    )
    field_comparison = {field: {
        "original": old_profile[field], "separated": new_profile[field],
        "equal": old_profile[field] == new_profile[field],
    } for field in profile_fields}
    return {
        "ad038": {
            "original": geometry(reference),
            "separated": geometry(separated),
            "mapped_relation_identity": identity_counts,
            "unscorable_relation_identity_count": sum(not item["all_required_references_scorable"] for item in relation_records),
            "paired_nearest_displacement_difference_population": paired,
            "paired_nearest_displacement_difference_statistics": stats(paired),
            "relation_records": relation_records,
        },
        "ad040": {
            "field_comparison": field_comparison,
            "relationship_population_count": {
                "original": len(old_profile["relationships"]),
                "separated": len(new_profile["relationships"]),
            },
            "correspondence_status_preserved": set(new_profile["correspondence_status_counts"]) == set(old_profile["correspondence_status_counts"]),
            "calibration_triad": separated["scientific_status"]["calibration"],
            "profile_structural_fields_compared": list(profile_fields),
        },
    }


def score() -> dict[str, object]:
    reference = json.loads(REFERENCE.read_text())
    result = {
        "execution_id": "EXEC-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01",
        "preregistration_id": "H-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01",
        "preregistration_fingerprint": "5c22ae45dcee9aee180a058e4015f4e748fa0acccf4dc374bfb1ae5af61fc62c",
        "reference_acceptance_id": "ACC-CEDVAL006-CANONICAL-RHYTHM-SECTION-REPORT-02",
        "reference_acceptance_fingerprint": "ea1490dc0171631381186b6728ee1b49ce5549041c38410b06132d021ee7e100",
        "scope_end": fraction_record(SCOPE_END),
        "runs": {},
        "firewall": {
            "latency_correction": "NONE", "h02_used": False, "strength_accessed": False,
            "physical_onset_error_claim": False, "musical_correspondence_claim": False,
            "universal_separator_quality_claim": False, "universal_jga_robustness_claim": False,
        },
    }
    original = {label: events(reference, label) for label in ("Drums", "Double Bass")}
    for run_name, path in REPORTS.items():
        report = json.loads(path.read_text())
        separated = {label: events(report, label) for label in ("Drums", "Double Bass")}
        mappings = {label: assign(original[label], separated[label]) for label in original}
        result["runs"][run_name] = {
            "canonical_report_scientific_fingerprint": report["scientific_fingerprint"],
            "level_1": {label: level1(original[label], separated[label], SCOPE_END) for label in original},
            "level_2": mappings,
            "level_3": level3(reference, report, mappings),
        }
    basis = dict(result)
    result["scoring_fingerprint"] = sha256(canonical(basis)).hexdigest()
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.write_bytes(canonical(score()) + b"\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
