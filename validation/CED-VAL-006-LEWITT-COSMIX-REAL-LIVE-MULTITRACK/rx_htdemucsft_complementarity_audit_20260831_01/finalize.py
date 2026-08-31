#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
source = HERE / "audit_execution_1.json"
result = json.loads(source.read_text())
(HERE / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != "artifact_manifest.json"}
(HERE / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
