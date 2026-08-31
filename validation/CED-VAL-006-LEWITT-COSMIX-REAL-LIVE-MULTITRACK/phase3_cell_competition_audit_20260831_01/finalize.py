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

p1, p2 = HERE / "audit_execution_1.json", HERE / "audit_execution_2.json"
assert p1.read_bytes() == p2.read_bytes()
audit = json.loads(p1.read_text())
audit_fp = audit.pop("audit_fingerprint")
assert sha256(canonical(audit)).hexdigest() == audit_fp
audit["audit_fingerprint"] = audit_fp
e = dict(audit["E_classification"])
classified_changed = e["previous_remains_new_candidate_displaces"] + e["previous_disappears_after_selects_new"] + e["previous_remains_after_selects_preexisting_other"]
e["previous_disappears_after_selects_preexisting_other"] = audit["population_counts"]["E_overlapping_A"] - classified_changed
assert e["previous_disappears_after_selects_preexisting_other"] == 3
result = {
    "audit_id": audit["audit_id"],
    "status": "COMPLETE_FROZEN",
    "protocol": {"commit": "c7eaef2", "fingerprint": audit["protocol_fingerprint"]},
    "population_counts": audit["population_counts"],
    "candidate_count_distributions": audit["candidate_count_distributions"],
    "C2_lost_match_classification": audit["C2_classification"],
    "E_changed_selection_classification": e,
    "D_processed_only_relationships": audit["D_relationships"],
    "new_candidate_displaced_retained_previous_selection": {"count": audit["newly_exposed_candidates_displacing_previous_selection_count"], "denominator_E": 232, "fraction_E": audit["newly_exposed_candidates_displacing_previous_selection_count"] / 232},
    "timing_consequences": audit["timing_groups"],
    "strength_authority": audit["strength_authority"],
    "dominant_mechanisms": [
        {"mechanism": "GROSS_RECOVERY_WITH_WIDE_DISPLACEMENT", "evidence": "B contributes 72.22790457342819% of processed matched squared displacement; median absolute displacement 0.031092970521541953 s and RMSE 0.06348290398089844 s."},
        {"mechanism": "PREVIOUS_CANDIDATE_DISAPPEARANCE", "evidence": "All 13 C2 losses and 225/232 E changes lost the previous selected coordinate; 222/232 E cases then selected a newly observable coordinate and 3 selected a previously observable alternate."},
        {"mechanism": "MULTI_CANDIDATE_COMPETITION_SECONDARY", "evidence": "69/232 E cells contained multiple processed candidates, but only 7/232 cases show a newly observable candidate displacing a previous selection that remained observable."}
    ],
    "future_non_ground_truth_intervention": audit["future_non_ground_truth_intervention"],
    "ground_truth_firewall": "Original-EME distance was used only to replay and describe frozen controlled-experiment assignments. It does not authorize a production closest-to-original rule.",
    "replay": {"complete_outputs_byte_identical": True, "execution_1_sha256": digest(p1), "execution_2_sha256": digest(p2), "audit_fingerprint_identical": True},
    "audit_fingerprint": audit_fp,
    "firewall": audit["firewall"],
}
result["result_record_fingerprint"] = sha256(canonical(result)).hexdigest()
(HERE / "result.json").write_bytes(canonical(result) + b"\n")
(HERE / "report.md").write_text(
    "# CED-VAL-006 Phase-3 Temporal-Cell Competition Audit\n\n"
    "Status: **COMPLETE — READ-ONLY — REPLAY VERIFIED**\n\n"
    "All 13 C2 cells changed from one candidate to zero; every previous selection disappeared. Among 232 E cells, 222 lost the previous selection and selected a newly observable coordinate, three lost it and selected a previously observable alternate, and seven retained it but selected a newly observable competitor. Only the last seven are direct new-candidate displacement of a still-observable prior selection.\n\n"
    "The 140 gross recoveries dominate timing error, contributing 72.22790457342819% of processed matched squared displacement. Candidate competition is secondary; candidate disappearance is the dominant explanation for C2 and E identity change.\n\n"
    "A future intervention without original-stem Ground Truth is INDETERMINATE because candidate strength or another non-Ground-Truth discriminator is not serialized. No closest-to-original rule is authorized. No audio, processing, JGA, matching, production code or historical evidence changed.\n\n"
    f"Audit fingerprint: `{audit_fp}`\n"
    f"Result-record fingerprint: `{result['result_record_fingerprint']}`\n"
)
names = ["audit_execution_1.json", "audit_execution_2.json", "finalize.py", "result.json", "report.md", "verify.py"]
manifest = {"audit_id": result["audit_id"], "audit_fingerprint": audit_fp, "result_record_fingerprint": result["result_record_fingerprint"], "repository_artifacts": {name: digest(HERE / name) for name in names if (HERE / name).exists()}}
(HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
print(audit_fp, result["result_record_fingerprint"])
