"""Verify frozen strength-max scoring and authority limitations."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_212608")
EXPECTED = "f9dd0c0892edbcab20782c4580baf64f6c8e7b2b36a87a1265fa80ecdf71d77e"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def main() -> None:
    result = json.loads((RUN / "scoring_result.json").read_text())
    scientific = result["scientific_content"]
    assert result["status"] == "PASS"
    assert result["scientific_fingerprint"] == EXPECTED
    assert sha256(canonical(scientific)).hexdigest() == EXPECTED
    cases = scientific["cases"]
    assert len(cases) == 56 and len({case["cell_identity"] for case in cases}) == 56
    assert sum(case["source"] == "Drums" for case in cases) == 54
    assert sum(case["source"] == "Double Bass" for case in cases) == 2
    assert all(case["scoring_status"] == "UNSCORABLE" for case in cases)
    assert all(case["scoring_reason"] == "AMBIGUOUS_MULTIPLE_OBSERVED" for case in cases)
    assert all(case["authorized_observed_eme_id"] is None for case in cases)
    assert all(not case["predictor_changed"] for case in cases)
    assert all(case["deterministic_replay_status"] == "EXACT_MATCH" for case in cases)
    assert scientific["overall_summary"] == {"total_cells": 56, "scorable_cells": 0, "unscorable_cells": 56, "STRENGTH_MAX_CORRECT": 0, "STRENGTH_MAX_INCORRECT": 0, "accuracy_scorable": None}
    assert scientific["classification"] == "INSUFFICIENT_SCORABLE_EVIDENCE"
    assert scientific["deterministic_replay"] and scientific["population_verified"]
    for flag in ("predictors_recomputed_after_ground_truth", "historical_h02_scores_changed", "historical_three_dataset_conclusion_changed", "h02_changed", "h03_created", "calibration_zero_changed", "raw_observations_changed", "production_promotion_authorized", "production_code_changed"):
        assert scientific[flag] is False
    print("PASS: 56 frozen predictors; 56 authority-limited UNSCORABLE cases; firewalls verified")


if __name__ == "__main__":
    main()
