"""Freeze checksums for the H02 out-of-sample validation artifacts."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_204545")
FILES = ("blind_execute.py", "blind_result.json", "blind_manifest.json", "score_frozen.py", "result.json", "verify.py", "report.md", "completion_protocol.json")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


payload = {"schema": "JGA-H02-OUT-OF-SAMPLE-ARTIFACT-MANIFEST/v1", "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02", "validation_dataset": "PR-CED-VAL-003-SWING-3-4-001", "blind_fingerprint": "a76e37eda621a266832a4fd347b9ac7334a3d12e2c94351dfdc5fa1dd9faa997", "scientific_fingerprint": "374ab02a71c0e583bba33b5723550c50c935f4d4fd11722085f1d368170d0987", "artifacts": {name: {"sha256": digest(BASE / name), "size_bytes": (BASE / name).stat().st_size} for name in FILES}}
(BASE / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(digest(BASE / "artifact_manifest.json"))
