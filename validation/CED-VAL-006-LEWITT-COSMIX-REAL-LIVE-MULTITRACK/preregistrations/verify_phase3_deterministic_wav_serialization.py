#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
path = HERE / "PR-CEDVAL006-PHASE3-DETERMINISTIC-WAV-SERIALIZATION-01.json"
record = json.loads(path.read_text())
content = dict(record)
expected = content.pop("preregistration_fingerprint")
canonical = json.dumps(content, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")
assert sha256(canonical).hexdigest() == expected
assert record["status"] == "PREREGISTERED_NOT_EXECUTED"
assert record["serialization"]["peak_policy"] == "PROHIBITED"
assert record["serialization"]["sample_transform"] == "NONE"
assert record["execution"]["independent_writes"] == 2
assert record["execution"]["whole_file_byte_identity_required"]
assert not any(record["firewall"].values())
utility = HERE / record["serialization"]["utility"]
assert sha256(utility.read_bytes()).hexdigest() == record["serialization"]["utility_sha256"]
print(json.dumps({"fingerprint": expected, "status": "PASS_NOT_EXECUTED"}, sort_keys=True))
