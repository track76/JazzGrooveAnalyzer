#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
path = HERE / "PR-CEDVAL006-PHASE3-POPULATION-TRANSITION-AUDIT-01.json"
record = json.loads(path.read_text())
content = dict(record)
expected = content.pop("preregistration_fingerprint")
actual = sha256(json.dumps(content, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest()
assert actual == expected
assert record["status"] == "PREREGISTERED_NOT_EXECUTED"
assert record["spectrum"]["bands_hz"] == [[20,80],[80,250],[250,1000],[1000,4000],[4000,"NYQUIST"]]
assert record["replay"]["executions"] == 2
assert record["replay"]["require_byte_identical_complete_output"]
assert not any(record["firewall"].values())
script = HERE / record["implementation"]["script"]
assert sha256(script.read_bytes()).hexdigest() == record["implementation"]["sha256"]
print(json.dumps({"fingerprint": actual, "status": "PASS_NOT_EXECUTED"}, sort_keys=True))
