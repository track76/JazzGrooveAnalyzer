"""Write the checksum manifest for the frozen calibration artifacts."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-002-SWING/run_20260823_170857")
FILES = (
    "build_symbolic_authority.py",
    "build_pair_authority.py",
    "experiment.py",
    "verify.py",
    "calibration_symbolic_events.json",
    "symbolic_pair_authority.json",
    "input_manifest.json",
    "event_level_results.json",
    "event_pair_results.json",
    "result.json",
    "report.md",
    "completion_protocol.json",
)


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


payload = {
    "schema": "JGA-CALIBRATION-ARTIFACT-MANIFEST/v1",
    "experiment_id": "H-CEDVAL002-CALIBRATION-ZERO-01",
    "scientific_fingerprint": "d4b0b18766cf2c69a367014704f2c2dc4429d977cdf8ddd27d767276b603d4e7",
    "artifacts": {name: {"sha256": checksum(BASE / name), "size_bytes": (BASE / name).stat().st_size} for name in FILES},
}
(BASE / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(checksum(BASE / "artifact_manifest.json"))
