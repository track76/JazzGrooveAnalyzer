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
assert result["population_counts"] == {"A":606,"B":140,"C1":296,"C2":13,"D":188,"E_overlapping_A":232,"net_matches":127}
assert result["C2_lost_match_classification"] == {"after_cell_empty":13,"previous_selected_disappeared":13,"previous_selected_remained_but_unselected":0}
e = result["E_changed_selection_classification"]
assert e["previous_disappears_after_selects_new"] == 222
assert e["previous_disappears_after_selects_preexisting_other"] == 3
assert e["previous_remains_new_candidate_displaces"] == 7
assert result["new_candidate_displaced_retained_previous_selection"]["count"] == 7
assert result["D_processed_only_relationships"]["no_authorized_original_cell"] == 0
assert result["future_non_ground_truth_intervention"]["status"] == "INDETERMINATE"
assert result["strength_authority"] == "UNAVAILABLE_NOT_SERIALIZED_BY_CANONICAL_REPORT"
assert result["replay"]["complete_outputs_byte_identical"]
assert (HERE / "audit_execution_1.json").read_bytes() == (HERE / "audit_execution_2.json").read_bytes()
assert not any(result["firewall"].values())
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
assert manifest["audit_fingerprint"] == result["audit_fingerprint"]
assert manifest["result_record_fingerprint"] == expected
for name, expected_digest in manifest["repository_artifacts"].items():
    assert digest(HERE / name) == expected_digest
print(json.dumps({"audit_fingerprint": result["audit_fingerprint"], "intervention": result["future_non_ground_truth_intervention"]["status"], "replay": "PASS_BYTE_IDENTICAL", "result_record_fingerprint": expected, "status": "PASS"}, sort_keys=True))
