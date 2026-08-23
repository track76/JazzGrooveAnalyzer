"""Freeze audit artifact checksums."""

from hashlib import sha256
import json
from pathlib import Path

base = Path(__file__).resolve().parent
names = ("audit.py", "audit_result.json", "verify.py", "report.md", "completion_protocol.json")
payload = {"schema": "JGA-SCORABILITY-AUDIT-ARTIFACT-MANIFEST/v1", "audit_id": "AUD-CEDVAL003-H02-SCORABILITY-01", "scientific_fingerprint": "34dafe335a0965ff2321bfc176386b974f1ee5a0425e153894e96bde8f939348", "artifacts": {name: {"sha256": sha256((base / name).read_bytes()).hexdigest(), "size_bytes": (base / name).stat().st_size} for name in names}}
(base / "artifact_manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
print(sha256((base / "artifact_manifest.json").read_bytes()).hexdigest())
