#!/usr/bin/env python3
"""Verify the frozen CED-VAL-006 Bass-preservation Phase-1 result."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


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
    stems = json.loads((HERE / "generated_stem_authority.json").read_text())
    stem_fingerprint = stems.pop("authority_fingerprint")
    require(stem_fingerprint == sha256(canonical(stems)).hexdigest(), "stem authority")
    for run, details in stems["runs"].items():
        for name, record in details["stems"].items():
            require(digest(Path(record["absolute_path"])) == record["sha256"], f"stem:{run}:{name}")
    require(stems["replay"] == {"B": "BYTE_IDENTICAL", "C": "BYTE_IDENTICAL"}, "separation replay")
    require((HERE / "scoring_execution_1.json").read_bytes() ==
            (HERE / "scoring_execution_2.json").read_bytes(), "scoring replay")
    require(result["decision_classification"] == "PERSISTENT_BASS_DEFICIT", "decision gate")
    require(result["persistence_gate_satisfied"] is True, "persistence")
    require(result["material_improvement_by_configuration"] == {"B": False, "C": False}, "improvement")
    require(not result["firewall"]["h02_used"] and not result["firewall"]["strength_used"], "scientific firewall")
    require(not result["firewall"]["production_code_changed"] and
            not result["firewall"]["alternative_models_executed"], "implementation firewall")
    print(json.dumps({
        "decision": "PERSISTENT_BASS_DEFICIT", "external_stems": "PASS",
        "result_fingerprint": fingerprint, "scoring_replay": "PASS_BYTE_IDENTICAL",
        "separation_replay_B": "BYTE_IDENTICAL", "separation_replay_C": "BYTE_IDENTICAL",
        "status": "PASS",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, RuntimeError) as exc:
        print(f"FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)
