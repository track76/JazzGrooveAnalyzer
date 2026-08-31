#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")
def digest(path): return sha256(path.read_bytes()).hexdigest()

p1, p2 = HERE / "capture_execution_1.json", HERE / "capture_execution_2.json"
assert p1.read_bytes() == p2.read_bytes()
study = json.loads(p1.read_text())
fp = study.pop("study_fingerprint")
assert sha256(canonical(study)).hexdigest() == fp
result = json.loads((HERE / "result.json").read_text())
result_fp = result.pop("result_record_fingerprint")
assert sha256(canonical(result)).hexdigest() == result_fp
assert result["study_fingerprint"] == fp
assert result["candidate_counts"] == {"unprocessed": 646, "processed": 934}
assert result["detector_unchanged"] is True
assert result["prospective_non_ground_truth_discriminator"] == "INDETERMINATE"
assert result["replay"]["execution_1_sha256"] == digest(p1) == digest(p2)
assert all(value is False for value in result["firewall"].values())
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
for name, expected in manifest["artifacts"].items():
    if name != "verify.py": assert digest(HERE / name) == expected
print("PASS", fp, result_fp)
