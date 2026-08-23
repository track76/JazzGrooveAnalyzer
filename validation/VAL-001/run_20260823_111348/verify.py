"""Independent integrity checks for H-VAL001-RHYTHM-CORRESPONDENCE-01."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


blind_manifest = json.loads((BASE / "blind_manifest.json").read_text())
blind = json.loads((BASE / "blind_result.json").read_text())
result = json.loads((BASE / "result.json").read_text())
manifest = json.loads((BASE / "artifact_manifest.json").read_text())
content = blind["scientific_content"]

assert digest(BASE / "blind_result.json") == blind_manifest["blind_result_sha256"]
assert blind["blind_scientific_fingerprint"] == blind_manifest["blind_scientific_fingerprint"]
assert content["population_counts"] == {"Drums": 63, "Double Bass": 27, "Piano": 49}
assert len(content["candidates"]) == 0
assert Counter(item["contributor"] for item in content["unresolved"]) == {"Piano": 49, "Double Bass": 27}
assert result["by_source"]["Piano"]["fn"] == 36
assert result["by_source"]["Double Bass"]["fn"] == 18
assert result["overall"]["tp"] == result["overall"]["fp"] == 0
assert result["overall"]["precision"] is None and result["overall"]["f1"] is None
assert result["overall"]["recall"] == 0.0
assert result["outcome_classification"] == "INSUFFICIENT_CANDIDATES"
assert result["raw_observations_modified"] is False
assert all(digest(BASE / name) == expected for name, expected in manifest.items())
print("PASS: blind freeze, scoring, raw immutability declarations, and artifact integrity")
