#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    h = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

score = json.loads((HERE / "scoring_execution_1.json").read_text())
summaries = {}
for run, value in score["runs"].items():
    bass = value["level_2"]["Double Bass"]
    drums = value["level_2"]["Drums"]
    ad038 = value["level_3"]["ad038"]
    summaries[run] = {
        "bass": {key: bass[key] for key in ("raw_original_count", "raw_separated_count", "matched_count", "original_only_count", "separated_only_count", "descriptive_precision", "descriptive_recall", "descriptive_f1", "absolute_displacement_statistics")},
        "drums_control": {key: drums[key] for key in ("raw_original_count", "raw_separated_count", "matched_count", "original_only_count", "separated_only_count", "descriptive_precision", "descriptive_recall", "descriptive_f1", "absolute_displacement_statistics")},
        "ad038": {"separated": {key: ad038["separated"][key] for key in ("eligible", "localized", "unresolved", "ties", "signed_statistics", "absolute_statistics")}, "mapped_relation_identity": ad038["mapped_relation_identity"], "unscorable_relation_identity_count": ad038["unscorable_relation_identity_count"], "paired_nearest_displacement_difference_statistics": ad038["paired_nearest_displacement_difference_statistics"]},
        "ad040": value["level_3"]["ad040"],
    }

baseline = {"eme_count": 646, "matched": 619, "original_only": 436, "separated_only": 27, "precision": 0.958204334365325, "recall": 0.5867298578199052, "f1": 0.7278071722516166, "median_absolute_seconds": 0.0068208616780045354, "rmse_seconds": 0.017893173606420704, "maximum_absolute_seconds": 0.18692063492063493}
population_pass = all(s["bass"]["matched_count"] > baseline["matched"] and s["bass"]["descriptive_recall"] > baseline["recall"] and s["bass"]["descriptive_f1"] > baseline["f1"] and s["bass"]["original_only_count"] < baseline["original_only"] for s in summaries.values())
timing_pass = all(s["bass"]["absolute_displacement_statistics"]["median"] <= baseline["median_absolute_seconds"] and s["bass"]["absolute_displacement_statistics"]["rmse"] <= baseline["rmse_seconds"] and s["bass"]["absolute_displacement_statistics"]["maximum"] <= baseline["maximum_absolute_seconds"] for s in summaries.values())
assert population_pass and not timing_pass
decision = "POPULATION_IMPROVEMENT_WITH_TIMING_DEGRADATION"
result = {
    "execution_id": "EXEC-CEDVAL006-BASS-PRESERVATION-PHASE3-REMEDIATED-01",
    "status": "COMPLETE_FROZEN",
    "phase3_preregistration": {"id": "H-CEDVAL006-BASS-PRESERVATION-PHASE3-DYNAMICS-01", "commit": "a6a8ed1fed6919cae9c1982602a6b9ac6b85fdda", "fingerprint": "17f7d3ea16de1cb2aefdd117290970b5b4057f27ec7d9f6c5dc5e5f8b06947a0"},
    "remediation": {"id": "PR-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01", "preregistration_commit": "e4a4f7f", "result_commit": "d30cf5c", "result_fingerprint": "44eeedd466541d2b4228fe2f8897a288dad8277ca4d71902ad66fc238e48effa", "byte_identical_wav_sha256": "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91", "decoded_samples_sha256": "433a07f34719abd1432080c4773185af89c4b91c01a4d11387db43ca46593c0c"},
    "canonical_reports": {f"run_{n}": {"sha256": digest(HERE / f"canonical_report_run_{n}.json"), "scientific_fingerprint": json.loads((HERE / f"canonical_report_run_{n}.json").read_text())["scientific_fingerprint"]} for n in (1, 2)},
    "scoring": {"fingerprint": score["scoring_fingerprint"], "execution_1_sha256": digest(HERE / "scoring_execution_1.json"), "execution_2_sha256": digest(HERE / "scoring_execution_2.json"), "byte_identical_replay": (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes(), "summaries": summaries},
    "original_bass_eme_authority": 1055,
    "unprocessed_htdemucs_ft": baseline,
    "population_improvement_gate": population_pass,
    "timing_preservation_gate": timing_pass,
    "stochastic_baseline_best_population_gate": all(s["bass"]["matched_count"] > 625 and s["bass"]["descriptive_recall"] > 0.5924170616113744 and s["bass"]["descriptive_f1"] > 0.7212925562608193 and s["bass"]["original_only_count"] < 430 for s in summaries.values()),
    "decision_classification": decision,
    "additional_original_bass_temporal_evidence_recovered": True,
    "bounded_interpretation": "More original Bass EME cells contain processed observations, but mandatory matched-event timing fidelity degraded; this is not CLEAR_DYNAMICS_IMPROVEMENT.",
    "firewall": {"phase3_transform_changed": False, "decision_criteria_changed": False, "detector_tuned": False, "eq_performed": False, "additional_condition_tested": False, "additional_model_tested": False, "preferred_run_selected": False, "runs_averaged": False, "jga_changed": False, "production_code_changed": False, "historical_evidence_modified": False, "phase4_started": False},
  }
result["result_fingerprint"] = sha256(canonical(result)).hexdigest()
(HERE / "result.json").write_bytes(canonical(result) + b"\n")
b = summaries["run_1"]["bass"]
(HERE / "report.md").write_text(
    "# CED-VAL-006 Bass Preservation Phase 3 Remediated Result\n\n"
    f"Decision: **{decision}**\n\n"
    f"Both runs produced {b['raw_separated_count']} Bass EME: {b['matched_count']} matched, {b['original_only_count']} original-only and {b['separated_only_count']} processed-only. Precision/recall/F1 are {b['descriptive_precision']}, {b['descriptive_recall']} and {b['descriptive_f1']}. Median absolute displacement, RMSE and maximum displacement are {b['absolute_displacement_statistics']['median']}, {b['absolute_displacement_statistics']['rmse']} and {b['absolute_displacement_statistics']['maximum']} seconds.\n\n"
    "The complete population tuple improved in both runs, recovering additional original Bass temporal evidence. All three mandatory timing bounds degraded, so CLEAR_DYNAMICS_IMPROVEMENT is prohibited. JGA, the transform, decision criteria, production code and historical evidence remained unchanged.\n\n"
    f"Result fingerprint: `{result['result_fingerprint']}`\n"
)
names = ["canonical_report_run_1.json", "canonical_report_run_2.json", "score.py", "scoring_execution_1.json", "scoring_execution_2.json", "finalize.py", "result.json", "report.md", "verify.py"]
manifest = {"execution_id": result["execution_id"], "result_fingerprint": result["result_fingerprint"], "repository_artifacts": {name: digest(HERE / name) for name in names if (HERE / name).exists()}, "external_processed_bass": {"run_1": "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91", "run_2": "ac612091d963bcd5673b96cf5b906589decf8f0c7201599a5c0903bbf3cddc91"}}
(HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
print(result["result_fingerprint"], decision)
