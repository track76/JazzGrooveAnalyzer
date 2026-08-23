"""Independently verify frozen strength-authority result invariants."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_211259")
RESULT = RUN / "strength_measurements.json"
EXPECTED_FINGERPRINT = "6903decbe3175db300002f148d5e4192f9c51ba8959a6534921675af753aa94d"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    scientific = result["scientific_content"]
    assert result["status"] == "PASS"
    assert sha256(canonical(scientific)).hexdigest() == EXPECTED_FINGERPRINT
    assert result["scientific_fingerprint"] == EXPECTED_FINGERPRINT
    records = scientific["records"]
    assert len(records) == 112
    assert len({record["eme_id"] for record in records}) == 112
    assert len({record["pulse_candidate_id"] for record in records}) == 112
    assert len({record["cell_identity"] for record in records}) == 56
    assert sum(record["source"] == "Drums" for record in records) == 108
    assert sum(record["source"] == "Double Bass" for record in records) == 4
    assert sum(record["source"] == "Piano" for record in records) == 0
    assert all(float.fromhex(record["strength_hex"]) == record["strength"] for record in records)
    assert all(float.fromhex(record["confidence_hex"]) == record["confidence"] for record in records)
    assert all(float.fromhex(record["timestamp_hex"]) == record["timestamp"] for record in records)
    assert all(record["replay_status"] == "EXACT_MATCH" for record in records)
    assert {record["confidence_hex"] for record in records} == {"0x1.0000000000000p+0"}
    assert scientific["lineage_join_failures"] == 0
    for flag in ("deterministic_replay", "exact_value_reproducibility", "within_source_measurement_authority"):
        assert scientific[flag] is True
    for flag in ("ground_truth_accessed", "selection_or_ranking_performed", "cross_source_comparability_authorized", "discrimination_authority", "historical_h02_scores_changed", "h02_changed", "h03_created", "calibration_zero_changed", "raw_observations_changed", "production_code_changed"):
        assert scientific[flag] is False
    print("PASS: 112/112 exact strength records; fingerprint and firewalls verified")


if __name__ == "__main__":
    main()
