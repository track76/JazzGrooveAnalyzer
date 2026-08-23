"""Freeze checksums for discriminability artifacts."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_212023")
FILES = ("execute.py", "input_manifest.json", "discriminability_result.json", "report.md", "verify.py", "completion_protocol.json")


def main() -> None:
    payload = {
        "schema": "JGA-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-MANIFEST/v1",
        "study_id": "H-CEDVAL003-WITHIN-CELL-STRENGTH-DISCRIMINABILITY-01",
        "scientific_fingerprint": "902c9a7dd53b7f99c103bbab9f39552017e930af03e5813a2cfafe6855abddcd",
        "artifacts": {name: sha256((RUN / name).read_bytes()).hexdigest() for name in FILES},
    }
    (RUN / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
