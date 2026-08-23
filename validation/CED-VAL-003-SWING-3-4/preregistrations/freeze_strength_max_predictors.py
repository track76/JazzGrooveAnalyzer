"""Freeze maximum identities without accessing Ground Truth."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4")
SOURCE = BASE / "run_20260823_212023/discriminability_result.json"
OUTPUT = BASE / "preregistrations/frozen_strength_max_predictors.json"
EXPECTED_SHA = "35904ceb0812fae6f7a1f67394735f313a2b079b79cf493c17298b76ce6e2d9c"
EXPECTED_FINGERPRINT = "902c9a7dd53b7f99c103bbab9f39552017e930af03e5813a2cfafe6855abddcd"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if digest(SOURCE) != EXPECTED_SHA:
        raise RuntimeError("Discriminability result checksum mismatch")
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    if result["scientific_fingerprint"] != EXPECTED_FINGERPRINT:
        raise RuntimeError("Discriminability fingerprint mismatch")
    predictors = []
    for cell in result["scientific_content"]["cells"]:
        if cell["status"] != "UNIQUE_STRENGTH_MAXIMUM" or cell["unique_maximum_observation"] is None:
            raise RuntimeError(f"Non-unique frozen predictor: {cell['cell_identity']}")
        predictors.append({
            "cell_identity": cell["cell_identity"],
            "cell_index": cell["cell_index"],
            "source": cell["source"],
            "contained_eme_ids": cell["contained_eme_ids"],
            "predicted_eme_id": cell["unique_maximum_observation"]["eme_id"],
            "predicted_pulse_candidate_id": cell["unique_maximum_observation"]["pulse_candidate_id"],
        })
    predictors.sort(key=lambda item: (item["source"], item["cell_index"], item["cell_identity"]))
    counts = {source: sum(item["source"] == source for item in predictors) for source in ("Drums", "Double Bass", "Piano")}
    if counts != {"Drums": 54, "Double Bass": 2, "Piano": 0} or len(predictors) != 56:
        raise RuntimeError("Frozen predictor population mismatch")
    payload = {
        "schema": "JGA-FROZEN-STRENGTH-MAX-PREDICTORS/v1",
        "source_scientific_fingerprint": EXPECTED_FINGERPRINT,
        "counts": counts,
        "predictors": predictors,
        "ground_truth_included": False,
        "h02_outcomes_included": False,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(digest(OUTPUT))


if __name__ == "__main__":
    main()
