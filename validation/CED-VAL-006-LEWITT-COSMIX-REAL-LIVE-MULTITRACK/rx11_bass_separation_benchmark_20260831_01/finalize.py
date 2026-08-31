#!/usr/bin/env python3
"""Freeze the preregistered RX11 Bass benchmark result without recomputation."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT / name).read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode()).hexdigest()


def main():
    assert (ROOT / "canonical_report_run_1.json").read_bytes() == (ROOT / "canonical_report_run_2.json").read_bytes()
    assert (ROOT / "scoring_execution_1.json").read_bytes() == (ROOT / "scoring_execution_2.json").read_bytes()
    evidence = load("operator_evidence.json")
    assert evidence["conformity"] == "PASS_BEFORE_JGA_ANALYSIS"
    scoring = load("scoring_execution_1.json")
    run = scoring["runs"]["run_1"]
    bass = run["level_2"]["Double Bass"]
    ad038 = run["level_3"]["ad038"]
    ad040 = run["level_3"]["ad040"]
    timing = bass["absolute_displacement_statistics"]
    demucs = {
        "eme_count": 646, "matched": 619, "original_only": 436, "separated_only": 27,
        "precision": 0.958204334365325, "recall": 0.5867298578199052,
        "f1": 0.7278071722516166, "median_absolute_displacement": 0.0068208616780045354,
        "timing_rmse": 0.017893173606420704, "maximum_displacement": 0.18692063492063493,
    }
    rx = {
        "eme_count": bass["raw_separated_count"], "matched": bass["matched_count"],
        "original_only": bass["original_only_count"], "rx_only": bass["separated_only_count"],
        "precision": bass["descriptive_precision"], "recall": bass["descriptive_recall"],
        "f1": bass["descriptive_f1"], "median_absolute_displacement": timing["median"],
        "timing_rmse": timing["rmse"], "maximum_displacement": timing["maximum"],
    }
    gates = {
        "clear_rx_improvement": {"matched_min": 672, "recall_min": 0.6367298578199052,
            "f1_min": 0.7528071722516166, "original_only_max": 383,
            "precision_min": 0.933204334365325, "timing_ratio_max": 1.10},
        "material_population_worsening": {"matched_max": 566, "recall_max": 0.5367298578199052,
            "f1_max": 0.7028071722516166, "original_only_min": 489},
        "timing_worsening_ratio": 1.25,
    }
    timing_ratios = {
        "median_absolute_displacement": rx["median_absolute_displacement"] / demucs["median_absolute_displacement"],
        "timing_rmse": rx["timing_rmse"] / demucs["timing_rmse"],
        "maximum_displacement": rx["maximum_displacement"] / demucs["maximum_displacement"],
    }
    classification = "WORSE_THAN_DEMUCS"
    reason = [
        "RX F1 is at or below the frozen material-population-worsening cutoff.",
        "Absent material population improvement, median displacement exceeds 125% of the frozen Demucs value.",
    ]
    result = {
        "result_id": "RES-CEDVAL006-RX11-BASS-SEPARATION-BENCHMARK-01",
        "preregistration_id": scoring["preregistration_id"],
        "preregistration_fingerprint": scoring["preregistration_fingerprint"],
        "scope": "frozen RX11 Bass output; unchanged JGA; frozen Level-1/2/3 retrospective comparison",
        "rx_file_authority": evidence["output"],
        "evidence_gate": {"status": "PASS", "source_record": evidence["evidence_record_id"]},
        "operator_evidence": {"operator": evidence["operator_identity"],
            "filesystem_export_timestamp_utc": evidence["filesystem_export_timestamp_utc"],
            "timestamp_classification": "FILESYSTEM_EXPORT_TIMESTAMP_UTC_NOT_MANUALLY_OBSERVED_OPERATOR_TIMESTAMP"},
        "rx_metrics": rx,
        "frozen_htdemucs_ft_reference": demucs,
        "comparison": {"rx_minus_demucs": {k: rx[k] - demucs[k] for k in
            ("eme_count", "matched", "original_only", "precision", "recall", "f1",
             "median_absolute_displacement", "timing_rmse", "maximum_displacement")},
            "timing_ratios": timing_ratios},
        "ad038": {"rx": {"eligible": ad038["separated"]["eligible"],
            "localized": ad038["separated"]["localized"], "ties": ad038["separated"]["ties"],
            "unresolved": ad038["separated"]["unresolved"],
            "absolute_nearest_displacement_statistics": ad038["separated"]["absolute_statistics"],
            "mapped_relation_identity": ad038["mapped_relation_identity"],
            "unscorable_relation_identity_count": ad038["unscorable_relation_identity_count"],
            "paired_nearest_displacement_difference_statistics": ad038["paired_nearest_displacement_difference_statistics"]}},
        "ad040": ad040,
        "decision": {"classification": classification, "reasons": reason, "frozen_gates": gates},
        "replay": {"status": "PASS_BYTE_IDENTICAL", "jga_runs": 2, "scoring_runs": 2,
            "canonical_report_sha256": sha(ROOT / "canonical_report_run_1.json"),
            "scoring_execution_sha256": sha(ROOT / "scoring_execution_1.json"),
            "canonical_report_scientific_fingerprint": scoring["runs"]["run_1"]["canonical_report_scientific_fingerprint"],
            "scoring_fingerprint": scoring["scoring_fingerprint"]},
        "scientific_firewall": scoring["firewall"],
    }
    result["result_fingerprint"] = canonical_hash(result)
    (ROOT / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    manifest = {p.name: sha(p) for p in sorted(ROOT.iterdir()) if p.is_file() and p.name != "artifact_manifest.json"}
    (ROOT / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
