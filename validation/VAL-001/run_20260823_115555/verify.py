"""Independent integrity checks for H-VAL001-RHYTHM-CORRESPONDENCE-02."""

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
assert Counter(item["contributor"] for item in content["candidates"]) == {"Piano": 12, "Double Bass": 1}
assert Counter(item["contributor"] for item in content["unresolved"]) == {"Piano": 37, "Double Bass": 26}
assert content["single_removed_condition"] == "EXACT_CROSS_SOURCE_SIGNATURE_EQUALITY"
assert result["by_source"]["Piano"]["tp"] == 11 and result["by_source"]["Piano"]["fp"] == 1
assert result["by_source"]["Double Bass"]["tp"] == 1 and result["by_source"]["Double Bass"]["fp"] == 0
assert result["overall"]["tp"] == 12 and result["overall"]["fp"] == 1 and result["overall"]["fn"] == 42
assert result["outcome_classification"] == "LOW_RECALL"
assert result["raw_observations_modified"] is False and result["production_code_modified"] is False
assert all(digest(BASE / name) == expected for name, expected in manifest.items())
print("PASS: blind freeze, scoring, scientific history, and artifact integrity")
