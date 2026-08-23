"""Freeze checksums for strength-authority artifacts."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_211259")
FILES = ("execute.py", "input_manifest.json", "strength_measurements.json", "report.md", "verify.py", "completion_protocol.json")


def main() -> None:
    artifacts = {name: sha256((RUN / name).read_bytes()).hexdigest() for name in FILES}
    payload = {
        "schema": "JGA-STRENGTH-MEASUREMENT-AUTHORITY-ARTIFACT-MANIFEST/v1",
        "study_id": "H-CEDVAL003-PULSECANDIDATE-STRENGTH-AUTHORITY-01",
        "scientific_fingerprint": "6903decbe3175db300002f148d5e4192f9c51ba8959a6534921675af753aa94d",
        "artifacts": artifacts,
    }
    (RUN / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
