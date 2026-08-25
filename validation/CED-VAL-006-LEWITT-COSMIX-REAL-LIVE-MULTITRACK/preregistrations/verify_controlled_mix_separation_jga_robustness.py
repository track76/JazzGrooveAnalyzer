#!/usr/bin/env python3
"""Verify the frozen controlled-mix separation/JGA preregistration."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RECORD = HERE / "H-CEDVAL006-CONTROLLED-MIX-SEPARATION-JGA-ROBUSTNESS-01.json"
MIX_AUTHORITY = HERE.parent / "controlled_mixdown_authority/controlled_mixdown_authority.json"
ACCEPTANCE = HERE.parent / "acceptance_20260825_113950/artifact_manifest.json"
RUNNER = ROOT / "src/jga/separation/demucs_runner.py"
CHECKPOINT = Path("/Users/StarTrack/.cache/torch/hub/checkpoints/955717e8-8726e21a.th")


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> int:
    record = json.loads(RECORD.read_text())
    fingerprint = record.pop("preregistration_fingerprint")
    computed = sha256(json.dumps(
        record, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")).hexdigest()
    require(fingerprint == computed, "preregistration fingerprint")
    mix = json.loads(MIX_AUTHORITY.read_text())
    require(mix["authority_fingerprint"] ==
            record["controlled_mix_authority"]["authority_fingerprint"],
            "controlled mix fingerprint")
    require(mix["output_asset"]["sha256"] ==
            record["controlled_mix_authority"]["sha256"], "controlled mix SHA-256")
    require(digest(Path(record["controlled_mix_authority"]["absolute_path"])) ==
            record["controlled_mix_authority"]["sha256"], "controlled mix asset")
    acceptance = json.loads(ACCEPTANCE.read_text())
    require(acceptance["acceptance_result_fingerprint"] ==
            record["reference_authority"]["acceptance_fingerprint"],
            "reference acceptance")
    require(digest(RUNNER) ==
            record["separation_contract"]["production_runner_sha256"],
            "production runner identity")
    require(digest(CHECKPOINT) ==
            record["separation_contract"]["checkpoint"]["sha256"],
            "checkpoint identity")
    require(subprocess.run(
        ("git", "rev-parse", "v0.3.0-alpha^{commit}"), cwd=ROOT,
        check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.strip() == record["jga_execution_contract"]["release_commit"],
            "JGA release authority")
    require(record["separation_contract"]["output_taxonomy"] ==
            ["drums.wav", "bass.wav", "other.wav", "vocals.wav"],
            "separation taxonomy")
    require(record["separation_contract"]["role_mapping"] == {
        "bass.wav": "Double Bass / ACCOMPANIMENT",
        "drums.wav": "Drums / TEMPORAL_REFERENCE",
    }, "role mapping")
    require(record["separation_replay"]["fresh_process_count"] == 2,
            "two-run replay")
    require(not any(record["architectural_firewall"].values()),
            "architectural firewall")
    require(record["status"] == "FROZEN_PREREGISTRATION_NOT_EXECUTED",
            "preregistration status")
    print(json.dumps({
        "controlled_mix": "PASS",
        "model_checkpoint": "PASS",
        "preregistration_fingerprint": fingerprint,
        "reference_acceptance": "PASS",
        "release": "PASS",
        "role_mapping": "PASS",
        "status": "PASS_NOT_EXECUTED",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
