#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
record = json.loads((HERE / "provider_evidence.json").read_text())
content = dict(record)
expected = content.pop("evidence_fingerprint")
actual = hashlib.sha256(
    json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
).hexdigest()
assert actual == expected
assert record["prospective_gate_assessment"] == "ACQUISITION_AUTHORITY_PARTIAL"
assessment = record["authority_assessment"]
assert assessment["same_performance"] == "ESTABLISHED_BY_PROVIDER_DECLARATION"
assert assessment["shared_hardware_clock"].startswith("UNESTABLISHED")
assert assessment["all_sample_level_transformations_absent"] == "NOT_ESTABLISHED"
assert assessment["physical_onset_ground_truth"] == "UNESTABLISHED"
assert not any(record[key] for key in (
    "historical_evidence_modified", "core_modified", "translation_modified",
    "domain_modified", "candidate_period_modified", "ad037_modified",
    "ad038_modified", "ad040_modified",
))
print(json.dumps({"evidence_fingerprint": actual, "status": "PASS"}, sort_keys=True))
