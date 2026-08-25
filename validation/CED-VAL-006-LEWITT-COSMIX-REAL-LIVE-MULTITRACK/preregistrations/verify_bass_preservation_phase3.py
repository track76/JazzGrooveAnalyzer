#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PATH = HERE / "H-CEDVAL006-BASS-PRESERVATION-PHASE3-DYNAMICS-01.json"
record = json.loads(PATH.read_text())
content = dict(record)
expected = content.pop("preregistration_fingerprint")
actual = hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
assert actual == expected
assert record["status"] == "PREREGISTERED_NOT_EXECUTED"
assert record["single_processing_condition"]["id"] == "STATIC_UPWARD_COMPRESSION_MINUS30DB_RATIO2_V1"
assert record["single_processing_condition"]["normalization"] == "NONE"
assert record["single_processing_condition"]["time_behavior"].startswith("MEMORYLESS_SAMPLE_SYNCHRONOUS")
assert record["future_execution"]["transform_runs"] == 2
assert not any(record["firewall"].values())
source = (HERE / "apply_phase3_dynamics.py").read_text()
assert "THRESHOLD = 10.0 ** (-30.0 / 20.0)" in source and "np.sqrt" in source
print(json.dumps({"fingerprint": actual, "status": "PASS_NOT_EXECUTED"}, sort_keys=True))
