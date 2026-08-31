#!/usr/bin/env python3
from hashlib import sha256
import json
from pathlib import Path
import soundfile as sf

HERE = Path(__file__).resolve().parent

def canonical(value):
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("ascii")

def digest(path):
    value = sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()

result = json.loads((HERE / "result.json").read_text())
expected = result.pop("result_fingerprint")
assert sha256(canonical(result)).hexdigest() == expected
result["result_fingerprint"] = expected
assert result["decision_classification"] == "INDETERMINATE"
assert result["transform_replay"]["required_byte_identical_output"]
assert not result["transform_replay"]["whole_file_byte_identical"]
assert result["transform_replay"]["decoded_sample_arrays_identical"]
payloads = []
for run in result["runs"].values():
    path = Path(run["output_path"])
    assert digest(path) == run["output_sha256"]
    data, rate = sf.read(path, dtype="float32", always_2d=True)
    assert sha256(data.tobytes()).hexdigest() == run["decoded_samples_sha256"]
    assert (rate, data.shape) == (44100, (10944947, 2))
    payloads.append(path.read_bytes())
assert payloads[0] != payloads[1]
assert [index + 1 for index, pair in enumerate(zip(*payloads)) if pair[0] != pair[1]] == [61]
assert result["jga_execution"].startswith("NOT_PERFORMED")
assert result["scoring_execution"].startswith("NOT_PERFORMED")
assert not any(result["firewall"].values())
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
assert manifest["result_fingerprint"] == expected
for name, expected_digest in manifest["repository_artifacts"].items():
    assert digest(HERE / name) == expected_digest
for run, expected_digest in manifest["external_complete_outputs"].items():
    assert digest(result["runs"][run]["output_path"]) == expected_digest
print(json.dumps({"decision": "INDETERMINATE", "result_fingerprint": expected, "transform_replay": "FAIL_WHOLE_FILE_BYTE_IDENTITY", "decoded_samples": "PASS_IDENTICAL", "status": "PASS_FROZEN_AUTHORITY_FAILURE"}, sort_keys=True))
