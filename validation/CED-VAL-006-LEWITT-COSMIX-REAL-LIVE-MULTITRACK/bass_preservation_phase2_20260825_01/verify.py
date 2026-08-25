#!/usr/bin/env python3
"""Verify the frozen CED-VAL-006 Bass-preservation Phase-2 result."""

from hashlib import sha256
import json
from pathlib import Path


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
assert result["preregistration"]["fingerprint"] == "8c17046b5b0ef8ea4bc6a88e3b2334e56b07b3ffaff9b5fea7a8b42d0acc1f48"
assert result["decision_classification"] == "MODEL_DEPENDENT_MIXED_RESULT"
assert not any(result["clear_model_improvement_by_model"].values())
assert result["scoring"]["byte_identical_replay"]
assert (HERE / "scoring_execution_1.json").read_bytes() == (HERE / "scoring_execution_2.json").read_bytes()
stems = json.loads((HERE / "generated_stem_authority.json").read_text())
stem_fp = stems.pop("authority_fingerprint")
assert sha256(canonical(stems)).hexdigest() == stem_fp == result["stem_authority_fingerprint"]
for replay in stems["replay"].values():
    assert replay == "BYTE_IDENTICAL"
for details in stems["runs"].values():
    for authority in details["stems"].values():
        assert digest(authority["absolute_path"]) == authority["sha256"]
        technical = authority["technical_audio"]
        assert (technical["encoding"], technical["bits_per_sample"], technical["channels"], technical["sample_rate_hz"], technical["frame_count"]) == ("IEEE_FLOAT", 32, 2, 44100, 10944947)
for summary in result["scoring"]["summaries"].values():
    assert summary["ad038"]["separated"]["unresolved"] == 0
    assert summary["ad040"]["correspondence_status_preserved"]
manifest = json.loads((HERE / "artifact_manifest.json").read_text())
assert manifest["result_fingerprint"] == expected
assert result["firewall"] == {"averaging": False, "h02_used": False, "latency_correction": "NONE", "preferred_run_selection": False, "production_code_changed": False, "stem_recombination": False, "strength_used": False}
print(json.dumps({"decision": result["decision_classification"], "result_fingerprint": expected, "scoring_replay": "PASS_BYTE_IDENTICAL", "separation_replay": stems["replay"], "status": "PASS"}, sort_keys=True))
