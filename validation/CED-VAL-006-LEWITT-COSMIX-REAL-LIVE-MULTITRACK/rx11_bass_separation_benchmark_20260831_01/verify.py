#!/usr/bin/env python3
"""Verify the frozen RX11 benchmark artifact set."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((ROOT / "result.json").read_text())
manifest = json.loads((ROOT / "artifact_manifest.json").read_text())
assert result["evidence_gate"]["status"] == "PASS"
assert result["decision"]["classification"] == "WORSE_THAN_DEMUCS"
assert result["replay"]["status"] == "PASS_BYTE_IDENTICAL"
assert result["rx_file_authority"]["sha256"] == "5588acd3d88e99a8aaca2c762b9a6a9a4fa263cdda03c7a56e2bc9b90b0fa26b"
assert result["operator_evidence"]["timestamp_classification"] == "FILESYSTEM_EXPORT_TIMESTAMP_UTC_NOT_MANUALLY_OBSERVED_OPERATOR_TIMESTAMP"
assert (ROOT / "canonical_report_run_1.json").read_bytes() == (ROOT / "canonical_report_run_2.json").read_bytes()
assert (ROOT / "scoring_execution_1.json").read_bytes() == (ROOT / "scoring_execution_2.json").read_bytes()
for name, expected in manifest.items():
    assert sha(ROOT / name) == expected, name
print("PASS: evidence, result, decision, manifest, and byte-identical replay verified")
