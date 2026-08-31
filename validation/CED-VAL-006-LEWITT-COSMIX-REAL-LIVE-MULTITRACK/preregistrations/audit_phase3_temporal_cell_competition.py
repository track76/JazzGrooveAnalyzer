#!/usr/bin/env python3
"""Frozen read-only temporal-cell competition audit."""

from fractions import Fraction
from hashlib import sha256
import argparse
import json
import math
from pathlib import Path
import statistics

DATASET = Path(__file__).resolve().parent.parent
PHASE2_SCORE = DATASET / "bass_preservation_phase2_20260825_01/scoring_execution_1.json"
PHASE3_SCORE = DATASET / "bass_preservation_phase3_remediated_20260831_01/scoring_execution_1.json"
UNPROCESSED_REPORT = DATASET / "bass_preservation_phase2_20260825_01/canonical_report_M1_run_1.json"
PROCESSED_REPORT = DATASET / "bass_preservation_phase3_remediated_20260831_01/canonical_report_run_1.json"
PROTOCOL = Path(__file__).resolve().parent / "PR-CEDVAL006-PHASE3-TEMPORAL-CELL-COMPETITION-AUDIT-01.json"
EXPECTED = {
    PHASE2_SCORE: "8534734ccb2eb84e18e80a92b54f801d0aff812bd59d12b32cb588aa6b1cc163",
    PHASE3_SCORE: "3923f17b1859204bfd6aa68b6843e99209cb35eba634b0dfb099311e9e321f48",
    UNPROCESSED_REPORT: "ac6a92c05c953cd25e911da9df5bc09fbaf86872ed70b2d39e301380a0508f17",
    PROCESSED_REPORT: "744b53a3cfeb30c1650892f27845f2a5e0d6d54dc92ab1075f03316f0c2cc542",
}

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    h = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def fraction(record):
    return Fraction(record["numerator"], record["denominator"])

def stats(values):
    values = sorted(float(value) for value in values)
    if not values:
        return {key: None for key in ("count", "minimum", "median", "maximum", "mean", "rmse")}
    return {"count": len(values), "minimum": min(values), "median": statistics.median(values), "maximum": max(values), "mean": statistics.fmean(values), "rmse": math.sqrt(statistics.fmean(value * value for value in values))}

def level2(path, run):
    return json.loads(path.read_text())["runs"][run]["level_2"]["Double Bass"]

def match_map(value):
    return {item["original_eme_id"]: item for item in value["matches"]}

def candidates(report_path):
    report = json.loads(report_path.read_text())
    authority = next(item for item in report["source_authorities"] if item["label"] == "Double Bass")
    observations = {item["pulse_candidate_id"]: item for item in report["observations"]["Double Bass"]}
    result = []
    for eme in report["elementary_metric_events"]:
        if eme["source_asset_sha256"] != authority["sha256"]:
            continue
        observation = observations[eme["supporting_pulse_candidate_ids"][0]]
        result.append({
            "eme_id": eme["eme_id"],
            "pulse_candidate_id": observation["pulse_candidate_id"],
            "timestamp_seconds": observation["timestamp_seconds"],
            "producer_sample_coordinate": observation["producer_sample_coordinate"],
            "producer_frame": observation["producer_frame"],
            "observation_index": observation["observation_index"],
            "strength": "UNAVAILABLE_NOT_SERIALIZED_BY_CANONICAL_REPORT",
        })
    return sorted(result, key=lambda item: (item["timestamp_seconds"], item["observation_index"]))

def selected(candidates_, original_time):
    return min(candidates_, key=lambda item: (abs(Fraction(item["producer_sample_coordinate"], 44100) - original_time), Fraction(item["producer_sample_coordinate"], 44100), item["observation_index"])) if candidates_ else None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for path, expected in EXPECTED.items():
        assert digest(path) == expected
    before = level2(PHASE2_SCORE, "M1_run_1")
    after_runs = json.loads(PHASE3_SCORE.read_text())["runs"]
    assert after_runs["run_1"]["level_2"]["Double Bass"] == after_runs["run_2"]["level_2"]["Double Bass"]
    after = after_runs["run_1"]["level_2"]["Double Bass"]
    before_map, after_map = match_map(before), match_map(after)
    before_ids, after_ids = set(before_map), set(after_map)
    A, B = before_ids & after_ids, after_ids - before_ids
    C2, C1 = before_ids - after_ids, {item["original_eme_id"] for item in after["original_only"]} - before_ids
    E = {identity for identity in A if before_map[identity]["separated_time"]["seconds"] != after_map[identity]["separated_time"]["seconds"]}
    original_records = {item["original_eme_id"]: item for item in [*before["matches"], *before["original_only"]]}
    before_candidates, after_candidates = candidates(UNPROCESSED_REPORT), candidates(PROCESSED_REPORT)
    cells = []
    candidate_to_cell = {}
    for original_id, authority in sorted(original_records.items(), key=lambda item: fraction(item[1]["original_time"])):
        original_time = fraction(authority["original_time"])
        left, right = fraction(authority["cell_left"]), fraction(authority["cell_right"])
        old = [item for item in before_candidates if left <= Fraction(item["producer_sample_coordinate"], 44100) < right]
        new = [item for item in after_candidates if left <= Fraction(item["producer_sample_coordinate"], 44100) < right]
        old_selected, new_selected = selected(old, original_time), selected(new, original_time)
        expected_old = before_map.get(original_id)
        expected_new = after_map.get(original_id)
        assert (old_selected is None) == (expected_old is None)
        assert (new_selected is None) == (expected_new is None)
        if old_selected:
            assert old_selected["timestamp_seconds"] == expected_old["separated_time"]["seconds"]
        if new_selected:
            assert new_selected["timestamp_seconds"] == expected_new["separated_time"]["seconds"]
        old_coords = {item["producer_sample_coordinate"] for item in old}
        new_coords = {item["producer_sample_coordinate"] for item in new}
        for item in new:
            candidate_to_cell[item["eme_id"]] = original_id
        classification = "C1_NEVER_MATCHED" if original_id in C1 else "C2_LOST" if original_id in C2 else "B_RECOVERED" if original_id in B else "A_RETAINED"
        changed = original_id in E
        previous_remains = old_selected is not None and old_selected["producer_sample_coordinate"] in new_coords
        after_selected_new = new_selected is not None and new_selected["producer_sample_coordinate"] not in old_coords
        newly_displaced_previous = bool(changed and previous_remains and after_selected_new)
        cells.append({
            "original_eme_id": original_id,
            "original_timestamp_seconds": float(original_time),
            "cell_left_seconds": float(left), "cell_right_seconds": float(right),
            "population": classification, "E_changed_selection": changed,
            "before_candidate_count": len(old), "after_candidate_count": len(new),
            "before_candidates": [{**item, "signed_distance_to_original_seconds": float(Fraction(item["producer_sample_coordinate"], 44100) - original_time), "selected": old_selected is not None and item["eme_id"] == old_selected["eme_id"]} for item in old],
            "after_candidates": [{**item, "signed_distance_to_original_seconds": float(Fraction(item["producer_sample_coordinate"], 44100) - original_time), "selected": new_selected is not None and item["eme_id"] == new_selected["eme_id"], "newly_observable_coordinate": item["producer_sample_coordinate"] not in old_coords} for item in new],
            "before_selected_coordinate": old_selected["producer_sample_coordinate"] if old_selected else None,
            "after_selected_coordinate": new_selected["producer_sample_coordinate"] if new_selected else None,
            "retained_coordinates": sorted(old_coords & new_coords),
            "new_coordinates": sorted(new_coords - old_coords),
            "disappeared_coordinates": sorted(old_coords - new_coords),
            "previous_selected_remains_observable": previous_remains,
            "after_selected_is_newly_observable": after_selected_new,
            "newly_observable_candidate_displaced_previous_selection": newly_displaced_previous,
        })
    by_id = {cell["original_eme_id"]: cell for cell in cells}
    d_records = after["separated_only"]
    d_relationship = {"retained_match_cell": 0, "gross_recovery_cell": 0, "lost_match_cell": 0, "changed_selection_cell": 0, "no_authorized_original_cell": 0, "cell_with_previous_selected_still_observable": 0}
    d_details = []
    for item in d_records:
        original_id = candidate_to_cell.get(item["separated_eme_id"])
        if original_id is None:
            d_relationship["no_authorized_original_cell"] += 1
            d_details.append({"processed_eme_id": item["separated_eme_id"], "cell": None})
            continue
        cell = by_id[original_id]
        d_relationship["retained_match_cell"] += original_id in A
        d_relationship["gross_recovery_cell"] += original_id in B
        d_relationship["lost_match_cell"] += original_id in C2
        d_relationship["changed_selection_cell"] += original_id in E
        d_relationship["cell_with_previous_selected_still_observable"] += cell["previous_selected_remains_observable"]
        d_details.append({"processed_eme_id": item["separated_eme_id"], "cell": original_id, "cell_population": cell["population"], "E_changed_selection": cell["E_changed_selection"]})
    affected = [cell for cell in cells if cell["population"] in {"C2_LOST", "B_RECOVERED"} or cell["E_changed_selection"] or cell["after_candidate_count"] > 1]
    count_distributions = {}
    for label, selected_cells in {
        "all_cells": cells, "affected_cells": affected,
        "C2_lost": [cell for cell in cells if cell["population"] == "C2_LOST"],
        "E_changed": [cell for cell in cells if cell["E_changed_selection"]],
    }.items():
        count_distributions[label] = {"cell_count": len(selected_cells), "before": {str(n): sum(cell["before_candidate_count"] == n for cell in selected_cells) for n in sorted({cell["before_candidate_count"] for cell in selected_cells})}, "after": {str(n): sum(cell["after_candidate_count"] == n for cell in selected_cells) for n in sorted({cell["after_candidate_count"] for cell in selected_cells})}}
    c2_cells = [cell for cell in cells if cell["population"] == "C2_LOST"]
    e_cells = [cell for cell in cells if cell["E_changed_selection"]]
    c2_classification = {"after_cell_empty": sum(cell["after_candidate_count"] == 0 for cell in c2_cells), "previous_selected_disappeared": sum(not cell["previous_selected_remains_observable"] for cell in c2_cells), "previous_selected_remained_but_unselected": sum(cell["previous_selected_remains_observable"] for cell in c2_cells)}
    e_classification = {
        "previous_remains_new_candidate_displaces": sum(cell["newly_observable_candidate_displaced_previous_selection"] for cell in e_cells),
        "previous_disappears_after_selects_new": sum(not cell["previous_selected_remains_observable"] and cell["after_selected_is_newly_observable"] for cell in e_cells),
        "previous_remains_after_selects_preexisting_other": sum(cell["previous_selected_remains_observable"] and not cell["after_selected_is_newly_observable"] for cell in e_cells),
        "after_multiple_candidates": sum(cell["after_candidate_count"] > 1 for cell in e_cells),
    }
    timing_groups = {}
    groups = {"B_RECOVERED": sorted(B), "E_CHANGED": sorted(E), "A_UNCHANGED_SELECTION": sorted(A - E)}
    total_sse = 0.0
    for label, ids in groups.items():
        values = [after_map[identity]["signed_displacement"]["seconds"] for identity in ids]
        sse = sum(value * value for value in values)
        total_sse += sse
        timing_groups[label] = {"count": len(values), "absolute_displacement": stats(map(abs, values)), "signed_displacement": stats(values), "squared_displacement_sum": sse}
    for group in timing_groups.values():
        group["processed_matched_sse_share"] = group["squared_displacement_sum"] / total_sse
    non_gt_attributes_available = any(item["strength"] != "UNAVAILABLE_NOT_SERIALIZED_BY_CANONICAL_REPORT" for item in after_candidates)
    intervention = "INDETERMINATE" if (e_classification["after_multiple_candidates"] or e_classification["previous_disappears_after_selects_new"]) and not non_gt_attributes_available else "NO"
    result = {
        "audit_id": "AUD-CEDVAL006-PHASE3-TEMPORAL-CELL-COMPETITION-01",
        "protocol_fingerprint": json.loads(PROTOCOL.read_text())["preregistration_fingerprint"],
        "authorities": {str(path.relative_to(DATASET)): expected for path, expected in EXPECTED.items()},
        "population_counts": {"A": len(A), "B": len(B), "C1": len(C1), "C2": len(C2), "D": len(d_records), "E_overlapping_A": len(E), "net_matches": len(B) - len(C2)},
        "candidate_count_distributions": count_distributions,
        "C2_classification": c2_classification,
        "E_classification": e_classification,
        "D_relationships": d_relationship,
        "newly_exposed_candidates_displacing_previous_selection_count": e_classification["previous_remains_new_candidate_displaces"],
        "timing_groups": timing_groups,
        "strength_authority": "UNAVAILABLE_NOT_SERIALIZED_BY_CANONICAL_REPORT",
        "future_non_ground_truth_intervention": {"status": intervention, "reason": "Competition/disappearance can be described from candidate timestamps, but the frozen reports preserve no candidate strength or other non-Ground-Truth attribute capable of selecting among candidates. Original-EME distance cannot authorize a production rule."},
        "complete_cell_records": cells,
        "D_candidate_records": d_details,
        "firewall": {"audio_modified": False, "processing_executed": False, "demucs_rerun": False, "jga_rerun": False, "matching_changed": False, "detector_tuned": False, "ground_truth_selection_rule_created": False, "timing_correction": False, "production_code_changed": False, "historical_evidence_modified": False, "phase4_started": False},
    }
    result["audit_fingerprint"] = sha256(canonical(result)).hexdigest()
    args.output.write_bytes(canonical(result) + b"\n")
    print(result["audit_fingerprint"])

if __name__ == "__main__":
    main()
