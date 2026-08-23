"""Verify frozen blind and post-freeze H02 out-of-sample evidence."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_204545")


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads((BASE / "blind_manifest.json").read_text())
    blind = json.loads((BASE / "blind_result.json").read_text())
    result = json.loads((BASE / "result.json").read_text())
    assert digest(BASE / "blind_result.json") == manifest["blind_result_sha256"]
    assert sha256(canonical(blind["scientific_content"])).hexdigest() == blind["blind_scientific_fingerprint"] == manifest["blind_scientific_fingerprint"]
    content = blind["scientific_content"]
    assert content["population_counts"] == {"Drums": 155, "Double Bass": 100, "Piano": 50}
    assert len(content["candidates"]) == 89 and len(content["unresolved"]) == 61
    assert len(content["candidates"]) + len(content["unresolved"]) == 150
    assert Counter(item["contributor"] for item in content["candidates"]) == {"Double Bass": 75, "Piano": 14}
    for record in content["candidates"]:
        assert not record["failure_reasons"] and record["status"] == "BLIND_CANDIDATE"
        assert record["nearest_selection_status"] == "UNIQUE"
        assert record["target_signature"] is not None and record["target_signature_recurrence"] >= 2
        assert record["drum_signature"] is not None and record["drum_signature_recurrence"] >= 2
    for source, payload in result["by_source"].items():
        assert payload["tp"] + payload["fp"] == payload["scorable_candidate_count"]
        assert payload["scorable_candidate_count"] + payload["ambiguous_unscorable_candidate_count"] == payload["blind_candidate_count"]
        assert payload["precision"] == payload["tp"] / (payload["tp"] + payload["fp"])
        assert payload["recall"] == payload["tp"] / (payload["tp"] + payload["fn"])
    overall = result["overall"]
    assert overall["tp"] == 29 and overall["fp"] == 4 and overall["fn"] == 15
    assert overall["ambiguous_unscorable_candidate_count"] == 56
    fingerprint_payload = dict(result)
    fingerprint = fingerprint_payload.pop("scientific_fingerprint")
    assert sha256(canonical(fingerprint_payload)).hexdigest() == fingerprint
    assert result["outcome_classification"] == "PARTIAL_CORRESPONDENCE_EVIDENCE"
    assert result["calibration_context_used_for_candidate_generation"] is False
    assert result["calibration_correction_applied"] is False
    assert result["raw_observations_modified"] is False
    assert result["production_code_modified"] is False
    print(f"STATUS=PASS\nBLIND_CANDIDATES=89\nTP=29\nFP=4\nFN=15\nSCIENTIFIC_FINGERPRINT={fingerprint}")


if __name__ == "__main__":
    main()
