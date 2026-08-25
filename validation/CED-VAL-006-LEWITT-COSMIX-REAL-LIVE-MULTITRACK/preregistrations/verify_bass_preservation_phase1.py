#!/usr/bin/env python3
"""Verify the frozen CED-VAL-006 Bass-preservation Phase-1 protocol."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RECORD = HERE / "H-CEDVAL006-BASS-PRESERVATION-PHASE1-01.json"
BASELINE = HERE.parent / "separation_robustness_20260825_01/result.json"
MIX = HERE.parent / "controlled_mixdown_authority/controlled_mixdown_authority.json"
RUNNER = ROOT / "src/jga/separation/demucs_runner.py"
EXECUTABLE = Path("/Users/StarTrack/Development/JGA-Demucs-env/bin/demucs")
CHECKPOINT = Path("/Users/StarTrack/.cache/torch/hub/checkpoints/955717e8-8726e21a.th")


def digest(path: Path) -> str:
    value = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def main() -> int:
    record = json.loads(RECORD.read_text())
    fingerprint = record.pop("preregistration_fingerprint")
    computed = sha256(json.dumps(record, ensure_ascii=True, allow_nan=False,
                                  sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest()
    require(fingerprint == computed, "preregistration fingerprint")
    baseline = json.loads(BASELINE.read_text())
    require(baseline["result_fingerprint"] == record["baseline_authority"]["result_fingerprint"], "baseline")
    mix = json.loads(MIX.read_text())
    require(mix["authority_fingerprint"] == record["ced_val_006_authorities"]["controlled_mix_fingerprint"], "mix fingerprint")
    require(mix["output_asset"]["sha256"] == record["ced_val_006_authorities"]["controlled_mix_sha256"], "mix SHA-256")
    authority = record["demucs_authority"]
    require(digest(RUNNER) == authority["production_runner_sha256"], "runner")
    require(digest(EXECUTABLE) == authority["demucs_executable_sha256"], "executable")
    require(digest(CHECKPOINT) == authority["checkpoint_sha256"], "checkpoint")
    require(subprocess.run(("git", "rev-parse", "v0.3.0-alpha^{commit}"), cwd=ROOT,
                           check=True, text=True, stdout=subprocess.PIPE).stdout.strip() ==
            record["jga_authority"]["release_commit"], "release")
    require(record["configurations"]["B_DETERMINISTIC_CANDIDATE"]["shifts"] == 0, "B shifts")
    require(record["configurations"]["C_DETERMINISTIC_HIGH_PRECISION_CANDIDATE"]["output_encoding"] == "FLOAT32_WAV", "C precision")
    require(record["replay_requirement"]["runs_per_candidate"] == 2, "two-run replay")
    require(not any(record["experiment_firewall"].values()), "experiment firewall")
    require(not any(record["architectural_firewall"].values()), "architecture firewall")
    require(record["deferred_models"]["download_authorized"] is False, "deferred downloads")
    require(record["status"] == "FROZEN_PREREGISTRATION_NOT_EXECUTED", "status")
    print(json.dumps({
        "baseline": "PASS", "controlled_mix": "PASS", "demucs": "PASS",
        "deferred_models": "PASS_NOT_AUTHORIZED", "experiment": "NOT_EXECUTED",
        "preregistration_fingerprint": fingerprint, "status": "PASS_NOT_EXECUTED",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
