"""Write the checksum manifest for the frozen calibration artifacts."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_203324")
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
    "experiment_id": "H-CEDVAL003-CALIBRATION-ZERO-01",
    "scientific_fingerprint": "589ee3c15783556bd0e5b7b6df53822dff56c1eddfb6d17476aa3152adef5270",
    "artifacts": {name: {"sha256": checksum(BASE / name), "size_bytes": (BASE / name).stat().st_size} for name in FILES},
}
(BASE / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(checksum(BASE / "artifact_manifest.json"))
