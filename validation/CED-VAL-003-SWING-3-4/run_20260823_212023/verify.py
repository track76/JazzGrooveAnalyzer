"""Verify within-cell strength discriminability result and firewalls."""

from hashlib import sha256
import json
from pathlib import Path


RUN = Path("validation/CED-VAL-003-SWING-3-4/run_20260823_212023")
EXPECTED = "902c9a7dd53b7f99c103bbab9f39552017e930af03e5813a2cfafe6855abddcd"


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def main() -> None:
    result = json.loads((RUN / "discriminability_result.json").read_text())
    scientific = result["scientific_content"]
    assert result["status"] == "PASS"
    assert result["scientific_fingerprint"] == EXPECTED
    assert sha256(canonical(scientific)).hexdigest() == EXPECTED
    cells = scientific["cells"]
    assert len(cells) == 56
    assert len({cell["cell_identity"] for cell in cells}) == 56
    assert sum(cell["source"] == "Drums" for cell in cells) == 54
    assert sum(cell["source"] == "Double Bass" for cell in cells) == 2
    assert all(len(cell["contained_eme_ids"]) == 2 for cell in cells)
    assert all(len(cell["contained_pulse_candidate_ids"]) == 2 for cell in cells)
    assert all(cell["status"] == "UNIQUE_STRENGTH_MAXIMUM" for cell in cells)
    assert all(cell["unique_maximum_observation"] is not None for cell in cells)
    assert all(cell["highest_minus_second_highest_strength"] > 0 for cell in cells)
    assert all(float.fromhex(cell["highest_minus_second_highest_strength_hex"]) == cell["highest_minus_second_highest_strength"] for cell in cells)
    assert all(cell["deterministic_replay_status"] == "EXACT_MATCH" for cell in cells)
    counts = scientific["counts_by_source"]
    assert counts["Drums"] == {"cells": 54, "UNIQUE_STRENGTH_MAXIMUM": 54, "STRENGTH_TIED": 0, "STRENGTH_UNRESOLVED": 0}
    assert counts["Double Bass"] == {"cells": 2, "UNIQUE_STRENGTH_MAXIMUM": 2, "STRENGTH_TIED": 0, "STRENGTH_UNRESOLVED": 0}
    assert scientific["exact_binary64_comparison"] and scientific["deterministic_replay"]
    for flag in ("threshold_or_tolerance_used", "cross_source_comparison_performed", "ground_truth_accessed", "correspondence_selection_performed", "historical_h02_scores_changed", "h02_changed", "h03_created", "calibration_zero_changed", "raw_observations_changed", "production_code_changed"):
        assert scientific[flag] is False
    print("PASS: 56/56 cells, exact classifications, fingerprint and firewalls verified")


if __name__ == "__main__":
    main()
