#!/usr/bin/env python3
"""Verify the frozen CED-VAL-006 separation robustness result chain."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                      separators=(",", ":")).encode("ascii")


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
    manifest = json.loads((HERE / "artifact_manifest.json").read_text())
    result = json.loads((HERE / "result.json").read_text())
    fingerprint = result.pop("result_fingerprint")
    require(fingerprint == sha256(canonical(result)).hexdigest(), "result fingerprint")
    for name, expected in manifest["repository_artifacts"].items():
        require(digest(HERE / name) == expected, f"artifact:{name}")
    generated = json.loads((HERE / "generated_stem_authority.json").read_text())
    generated_fingerprint = generated.pop("authority_fingerprint")
    require(generated_fingerprint == sha256(canonical(generated)).hexdigest(), "stem authority fingerprint")
    for run, stems in generated["runs"].items():
        for name, record in stems["stems"].items():
            require(digest(Path(record["absolute_path"])) == record["sha256"], f"stem:{run}:{name}")
    require((HERE / "scoring_execution_1.json").read_bytes() ==
            (HERE / "scoring_execution_2.json").read_bytes(), "scoring replay")
    require(generated["replay_classification"] == "SCIENTIFICALLY_NONIDENTICAL", "separation replay")
    require(subprocess.run(("git", "rev-parse", "v0.3.0-alpha^{commit}"), cwd=ROOT,
                           check=True, text=True, stdout=subprocess.PIPE).stdout.strip() ==
            "c7b9b65362303ff17c48897c4d26a518595fe9c5", "JGA release")
    require(not any(result["firewall"][key] for key in (
        "h02_used", "strength_accessed", "production_code_changed", "core_changed",
        "translation_changed", "domain_changed", "candidate_period_changed",
        "controlled_mix_changed", "provider_raw_assets_changed",
    )), "firewall")
    print(json.dumps({
        "external_stems": "PASS", "result_fingerprint": fingerprint,
        "scoring_replay": "PASS_BYTE_IDENTICAL", "separation_replay": "SCIENTIFICALLY_NONIDENTICAL",
        "status": "PASS",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
