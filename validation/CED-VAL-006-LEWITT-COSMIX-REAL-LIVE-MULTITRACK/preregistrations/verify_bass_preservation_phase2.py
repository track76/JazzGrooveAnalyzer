#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORD = HERE / "H-CEDVAL006-BASS-PRESERVATION-PHASE2-01.json"
ROOT = HERE.parents[2]
RESULT = ROOT / "validation/CED-VAL-006-LEWITT-COSMIX-REAL-LIVE-MULTITRACK/bass_preservation_phase1_20260825_01/result.json"
CACHE = Path("/Users/StarTrack/.cache/huggingface/hub")
REPOS = {
    "htdemucs_ft": CACHE / "models--adefossez--HTDemucs-ft/snapshots/478be8a68f85418addd6f7baefd4be76522a4034",
    "htdemucs_6s": CACHE / "models--adefossez--HTDemucs-6s/snapshots/053e1404489b3dc58bf718224fac4b7316de8c93",
    "mdx_extra": CACHE / "models--adefossez--Demucs-mdx_extra/snapshots/878043a2fbced47a17d05c790a361a9f01599a6e",
}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def canonical_fingerprint(record):
    content = dict(record)
    content.pop("preregistration_fingerprint", None)
    raw = json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()

record = json.loads(RECORD.read_text())
assert record["status"] == "PREREGISTERED_NOT_EXECUTED"
assert record["authorities"]["phase1_fingerprint"] == "7312b5d9dbbf30aa45e9d01c5e7134a45c81bfb15dc938db30d92529d106f848"
assert json.loads(RESULT.read_text())["result_fingerprint"] == record["authorities"]["phase1_fingerprint"]
assert set(m["name"] for m in record["models"].values()) == {"htdemucs_ft", "htdemucs_6s", "mdx_extra"}
for model in record["models"].values():
    base = REPOS[model["name"]]
    assert sha(base / model["manifest"]["file"]) == model["manifest"]["sha256"]
    for checkpoint in model["checkpoints"]:
        assert sha(base / checkpoint["file"]) == checkpoint["sha256"]
    assert "drums" in model["taxonomy"] and "bass" in model["taxonomy"]
assert record["models"]["M2"]["taxonomy"] == ["drums", "bass", "other", "vocals", "guitar", "piano"]
assert record["execution_contract"]["runs_per_model"] == 2
assert record["execution_contract"]["common_arguments"] == ["-d", "cpu", "--shifts", "0", "--overlap", "0.25", "-j", "0", "--float32"]
assert record["deferred_hypothesis"]["status"] == "DEFERRED_TO_PHASE_3"
assert not any(record["firewall"].values())
fingerprint = canonical_fingerprint(record)
assert fingerprint == record["preregistration_fingerprint"]
print(json.dumps({"fingerprint": fingerprint, "model_authority": "PASS", "status": "PASS_NOT_EXECUTED"}, sort_keys=True))
