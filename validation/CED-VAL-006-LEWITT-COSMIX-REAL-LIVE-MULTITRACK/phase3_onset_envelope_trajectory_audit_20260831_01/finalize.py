#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
def canonical(value): return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")
def digest(path): return sha256(path.read_bytes()).hexdigest()

r1, r2 = HERE / "run_1", HERE / "run_2"
names1, names2 = sorted(x.name for x in r1.iterdir()), sorted(x.name for x in r2.iterdir())
assert names1 == names2
for name in names1: assert (r1/name).read_bytes() == (r2/name).read_bytes(), name
audit = json.loads((r1/"audit.json").read_text())
audit_fp = audit.pop("audit_fingerprint")
assert sha256(canonical(audit)).hexdigest() == audit_fp
audit["audit_fingerprint"] = audit_fp
result = {
    "audit_id": audit["audit_id"], "status": "COMPLETE_FROZEN",
    "protocol": {"commit": "3a35920", "fingerprint": audit["protocol_fingerprint"]},
    "neighborhood": audit["neighborhood"],
    "transition_results": audit["transition_results"],
    "subgroup_results": audit["subgroup_results"],
    "combined_primary_mechanisms": audit["combined_primary_mechanisms"],
    "peak_relocation": {key: {"relocated_count": value["dominant_peak_relocated_count"], "absolute_shift_frames": value["absolute_dominant_peak_shift_frames"]} for key,value in audit["transition_results"].items()},
    "local_maximality": {key: {"gained": value["local_maximality_gained_count"], "lost": value["local_maximality_lost_count"]} for key,value in audit["transition_results"].items()},
    "peak_rank": {key: value["rank_change"] for key,value in audit["transition_results"].items()},
    "dominant_mechanism": audit["dominant_mechanism"],
    "explanatory_scope": {"explained_fraction": audit["explained_fraction"], "interpretation": "All coordinate transitions are reproducible consequences of native peak-pick conditions under the frozen precedence; the heterogeneous mechanism mixture does not authorize a single prospective principle under the preregistered gate."},
    "prospective_non_ground_truth_principle": audit["prospective_non_ground_truth_principle"],
    "principle": audit["principle"],
    "diagnostic_plots": [{**x, "canonical_path": f"run_1/{x['filename']}"} for x in audit["diagnostic_plots"]],
    "plot_selection_rule": "Lowest sample coordinate in every observed primary transition mechanism and in B/C2/E-before/E-after, deduplicated by coordinate in sorted selection-class order.",
    "replay": {"status": "PASS_BYTE_IDENTICAL", "complete_json_byte_identical": True, "all_corresponding_pngs_byte_identical": True, "run_1_audit_sha256": digest(r1/"audit.json"), "run_2_audit_sha256": digest(r2/"audit.json"), "artifact_count_per_run": len(names1)},
    "audit_fingerprint": audit_fp,
    "firewall": audit["firewall"],
}
result["result_record_fingerprint"] = sha256(canonical(result)).hexdigest()
(HERE/"result.json").write_bytes(canonical(result)+b"\n")
(HERE/"report.md").write_text(
    "# CED-VAL-006 Phase-3 Native Onset-Envelope Trajectory Audit\n\n"
    "Status: **COMPLETE — READ-ONLY — REPLAY VERIFIED**\n\n"
    "The fixed 17-frame (plus/minus eight-frame) trajectories explain all 250 disappearing and 538 newly observable coordinate transitions under the preregistered detector-native precedence. The combined primary counts are: adaptive-threshold change 255, local-peak relocation 247, local-maximality change 154, and wait/rank competition 132.\n\n"
    "The mechanism is heterogeneous. The largest component, adaptive-threshold change, accounts for only 32.3604%, below the frozen 40% single-mechanism gate. The prospective non-Ground-Truth outcome is therefore `INDETERMINATE`; no principle or selection rule is authorized.\n\n"
    "All seven deterministic diagnostic PNGs replay byte-identically. Audio, processing, detector, candidates, matching, temporal cells, JGA production code, semantic authorities and historical evidence were unchanged.\n\n"
    f"Audit fingerprint: `{audit_fp}`\n"
    f"Result-record fingerprint: `{result['result_record_fingerprint']}`\n"
)
tracked = [x for x in HERE.rglob("*") if x.is_file() and x.name != "artifact_manifest.json"]
manifest = {"audit_id": result["audit_id"], "audit_fingerprint": audit_fp, "result_record_fingerprint": result["result_record_fingerprint"], "artifacts": {str(x.relative_to(HERE)): digest(x) for x in sorted(tracked)}}
(HERE/"artifact_manifest.json").write_bytes(canonical(manifest)+b"\n")
print(audit_fp, result["result_record_fingerprint"])
