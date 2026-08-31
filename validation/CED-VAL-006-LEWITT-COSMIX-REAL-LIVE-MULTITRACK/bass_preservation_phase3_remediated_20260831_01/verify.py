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
expected = result.pop("result_fingerprint")
assert sha256(canonical(result)).hexdigest() == expected
result["result_fingerprint"] = expected
assert result["decision_classification"] == "POPULATION_IMPROVEMENT_WITH_TIMING_DEGRADATION"
assert result["population_improvement_gate"]
assert not result["timing_preservation_gate"]
assert result["additional_original_bass_temporal_evidence_recovered"]
assert result["scoring"]["byte_identical_replay"]
assert (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes()
for summary in result["scoring"]["summaries"].values():
    bass = summary["bass"]
    assert (bass["raw_separated_count"], bass["matched_count"], bass["original_only_count"], bass["separated_only_count"]) == (934, 746, 309, 188)
    assert summary["ad038"]["separated"]["unresolved"] == 0
    assert summary["ad040"]["correspondence_status_preserved"]
assert not any(result["firewall"].values())
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
assert manifest["result_fingerprint"] == expected
for name, expected_digest in manifest["repository_artifacts"].items():
    assert digest(HERE / name) == expected_digest
print(json.dumps({"decision": result["decision_classification"], "result_fingerprint": expected, "scoring_replay": "PASS_BYTE_IDENTICAL", "status": "PASS"}, sort_keys=True))
