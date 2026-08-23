"""Freeze strength-max validation artifact checksums."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_212608")
FILES = ("score.py", "input_manifest.json", "scoring_result.json", "report.md", "verify.py", "completion_protocol.json")


def main() -> None:
    payload = {
        "schema": "JGA-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-MANIFEST/v1",
        "study_id": "H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01",
        "scientific_fingerprint": "f9dd0c0892edbcab20782c4580baf64f6c8e7b2b36a87a1265fa80ecdf71d77e",
        "artifacts": {name: sha256((RUN / name).read_bytes()).hexdigest() for name in FILES},
    }
    (RUN / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
