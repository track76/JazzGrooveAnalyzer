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

result = json.loads((HERE / "result.json").read_text())
expected = result.pop("result_record_fingerprint")
assert sha256(canonical(result)).hexdigest() == expected
result["result_record_fingerprint"] = expected
assert result["evidence_conflict_resolution"]["resolved"]
assert (result["evidence_conflict_resolution"]["gross_recovered"], result["evidence_conflict_resolution"]["lost_prior_matches"], result["evidence_conflict_resolution"]["net_additional_matches"]) == (140, 13, 127)
assert result["C_subgroups"]["never_matched"]["count"] == 296
assert result["C_subgroups"]["previously_matched_lost_after_processing"]["count"] == 13
assert result["populations"]["E_MATCH_IDENTITY_CHANGED"]["count"] == 232
assert result["E_overlap_status"].startswith("OVERLAPPING")
assert result["eq_hypothesis_status"] == "NO"
assert result["eq_hypothesis_regions"] == []
assert result["replay"]["complete_outputs_byte_identical"]
assert (HERE / "audit_execution_1.json").read_bytes() == (HERE / "audit_execution_2.json").read_bytes()
assert not any(result["firewall"].values())
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
assert manifest["audit_fingerprint"] == result["audit_fingerprint"]
assert manifest["result_record_fingerprint"] == expected
for name, expected_digest in manifest["repository_artifacts"].items():
    assert digest(HERE / name) == expected_digest
print(json.dumps({"audit_fingerprint": result["audit_fingerprint"], "replay": "PASS_BYTE_IDENTICAL", "result_record_fingerprint": expected, "status": "PASS"}, sort_keys=True))
