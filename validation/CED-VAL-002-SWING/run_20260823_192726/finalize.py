"""Freeze checksums for the H02 out-of-sample validation artifacts."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-002-SWING/run_20260823_192726")
FILES = ("blind_execute.py", "blind_result.json", "blind_manifest.json", "score_frozen.py", "result.json", "verify.py", "report.md", "completion_protocol.json")


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


payload = {"schema": "JGA-H02-OUT-OF-SAMPLE-ARTIFACT-MANIFEST/v1", "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02", "validation_dataset": "PR-CED-VAL-002-SWING-002", "blind_fingerprint": "c053888ade8ddba30dad9abd11f4486dd9083640307d5c49feb409c389e28c08", "scientific_fingerprint": "ac6df971b4d1fb224c2324fb91cac85c04bb30062f86103f5681293dcd80c89e", "artifacts": {name: {"sha256": digest(BASE / name), "size_bytes": (BASE / name).stat().st_size} for name in FILES}}
(BASE / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(digest(BASE / "artifact_manifest.json"))
