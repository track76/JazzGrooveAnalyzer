#!/usr/bin/env python3
from collections import Counter, defaultdict
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def stats(values):
    values = sorted(float(x) for x in values)
    if not values:
        return {"count": 0, "minimum": None, "median": None, "maximum": None, "mean": None, "population_sd": None}
    return {"count": len(values), "minimum": values[0], "median": statistics.median(values), "maximum": values[-1], "mean": statistics.fmean(values), "population_sd": statistics.pstdev(values)}

p1, p2 = HERE / "capture_execution_1.json", HERE / "capture_execution_2.json"
assert p1.read_bytes() == p2.read_bytes()
study = json.loads(p1.read_text())
fingerprint = study.pop("study_fingerprint")
assert sha256(canonical(study)).hexdigest() == fingerprint
study["study_fingerprint"] = fingerprint

disappearing = defaultdict(list)
for item in study["disappearing_coordinates"]["records"]:
    disappearing[item["population"]].append(item["native_onset_strength"])
new = defaultdict(list)
for item in study["newly_observable_coordinates"]["records"]:
    new[item["population"]].append(item["native_onset_strength"])
multi = defaultdict(list)
for item in study["multi_candidate_relationships"]["records"]:
    multi[item["population"]].append(item)

coordinate_characterization = {
    "disappearing_by_population": {key: stats(disappearing[key]) for key in ("A_UNCHANGED", "B", "C1", "C2", "E")},
    "newly_observable_by_population": {key: stats(new[key]) for key in ("A_UNCHANGED", "B", "C1", "C2", "E")},
    "multi_candidate_by_population": {
        key: {
            "cell_count": len(multi[key]),
            "selected_unique_strength_maximum_count": sum(x["selected_is_unique_strength_maximum"] for x in multi[key]),
            "selected_unique_strength_maximum_rate": (sum(x["selected_is_unique_strength_maximum"] for x in multi[key]) / len(multi[key])) if multi[key] else None,
            "selected_minus_strongest_other": stats(x["selected_strength"] - x["maximum_other_strength"] for x in multi[key]),
        } for key in ("A_UNCHANGED", "B", "C1", "C2", "E")
    },
}

result = {
    "study_id": study["study_id"],
    "status": "COMPLETE_FROZEN",
    "protocol": {"commit": "163d2ae", "fingerprint": study["protocol_fingerprint"]},
    "input_authorities": study["input_authorities"],
    "detector_unchanged": True,
    "native_evidence_captured": study["native_evidence_captured"],
    "candidate_counts": study["candidate_counts"],
    "population_strength_characterization": study["population_strength_characterization"],
    "coordinate_characterization": coordinate_characterization,
    "all_disappearing_coordinates": {key: value for key, value in study["disappearing_coordinates"].items() if key != "records"},
    "all_newly_observable_coordinates": {key: value for key, value in study["newly_observable_coordinates"].items() if key != "records"},
    "multi_candidate_strength_relationships": {key: value for key, value in study["multi_candidate_relationships"].items() if key != "records"},
    "candidate_disappearance_explanation": "NOT_ESTABLISHED_BY_NATIVE_STRENGTH_ALONE: disappearing candidates had observable pre-transform native strength, but the capture does not preserve a counterfactual processed envelope value at coordinates that ceased to be detector candidates.",
    "B_wide_displacement_explanation": "PARTIALLY_SUPPORTED: all 140 B selections are newly observable coordinates and their processed strength is lower than D in aggregate (Cliff's delta -0.34817629179331305), but native strength alone neither locates the latent pre-transform evidence nor explains temporal displacement from original EME authority.",
    "prospective_non_ground_truth_discriminator": study["prospective_non_ground_truth_discriminator"],
    "prospective_principle": None,
    "discriminator_evidence": study["descriptive_discriminator_evidence"],
    "replay": {"status": "PASS_BYTE_IDENTICAL", "execution_1_sha256": digest(p1), "execution_2_sha256": digest(p2), "complete_outputs_byte_identical": True, "study_fingerprint_identical": True},
    "study_fingerprint": fingerprint,
    "firewall": study["firewall"],
}
result["result_record_fingerprint"] = sha256(canonical(result)).hexdigest()
(HERE / "result.json").write_bytes(canonical(result) + b"\n")
(HERE / "report.md").write_text(
    "# CED-VAL-006 Phase-3 Detector-Native Evidence Capture\n\n"
    "Status: **COMPLETE — VALIDATION-ONLY — REPLAY VERIFIED**\n\n"
    "The unchanged JGA source-specific detector reproduced 646 unprocessed and 934 processed Bass candidates and captured native frame, frame-start sample coordinate, timestamp, onset-envelope strength and confidence. All coordinates exactly matched the frozen canonical reports.\n\n"
    "Native strength does not pass the preregistered prospective-discriminator gate. B recovered candidates have median strength 1.7448078989982605 versus 2.02143657207489 for D, with Cliff's delta -0.34817629179331305. In 164 processed multi-candidate cells the frozen selected candidate was the unique strength maximum in 106 (64.63414634146342%), below the 75% gate. The outcome is `INDETERMINATE`; no selection principle is authorized.\n\n"
    "All 13 C2 prior coordinates are among the disappearing population. Native strength confirms they were detector-observable before processing, but does not establish why they disappeared because no invented counterfactual score was computed. All 140 B selections are newly observable; strength alone does not explain their wide original-authority displacement.\n\n"
    f"Study fingerprint: `{fingerprint}`\n"
    f"Result-record fingerprint: `{result['result_record_fingerprint']}`\n"
)
names = ["capture_execution_1.json", "capture_execution_2.json", "finalize.py", "result.json", "report.md", "verify.py"]
manifest = {"study_id": result["study_id"], "study_fingerprint": fingerprint, "result_record_fingerprint": result["result_record_fingerprint"], "artifacts": {name: digest(HERE / name) for name in names if (HERE / name).exists()}}
(HERE / "artifact_manifest.json").write_bytes(canonical(manifest) + b"\n")
print(fingerprint, result["result_record_fingerprint"])
