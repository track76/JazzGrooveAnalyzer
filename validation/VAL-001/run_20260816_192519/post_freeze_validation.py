"""Post-freeze Ground Truth comparison; never participates in discovery."""

from __future__ import annotations

import hashlib
import json
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN_DIR = Path(__file__).resolve().parent
BLIND = RUN_DIR / "blind_result.json"
FREEZE = RUN_DIR / "blind_freeze.json"
GROUND_TRUTH = ROOT / "validation/VAL-001/run_20260809_065633/baseline.json"
BLIND_SHA256 = "0f6d8162053142893d4f938f32c73174b26dd8c783a457ad98e6e491ecb369cd"
FREEZE_SHA256 = "7e4809ff036089c466a81e6ce82cac31c5b0cc937555c525114bb309f89e8a01"
GROUND_TRUTH_SHA256 = "9f219660d933b9084190708b8b7ae9ef092c987aff767390750351e83a93090d"
SAMPLE_RATE = Decimal(44100)
FRAME_LENGTH = Decimal(512)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if sha256(BLIND) != BLIND_SHA256 or sha256(FREEZE) != FREEZE_SHA256:
    raise RuntimeError("Blind freeze integrity failure")
if sha256(GROUND_TRUTH) != GROUND_TRUTH_SHA256:
    raise RuntimeError("Ground Truth identity mismatch")

blind = json.loads(BLIND.read_text())
ground_truth_record = json.loads(GROUND_TRUTH.read_text())["ground_truth"]
rate = Decimal(ground_truth_record["tempo"]["beats_per_minute"])
period = Decimal(60) / rate
period_frames = period * SAMPLE_RATE / FRAME_LENGTH

comparisons = []
for candidate in blind["common_period_candidates"]:
    lower, upper = (Decimal(value) for value in candidate["common_measurement_intersection_frames"])
    if lower <= period_frames <= upper:
        relation = "GROUND_TRUTH_REFERENCE_PERIOD_WITHIN_MEASUREMENT_INTERVAL"
    elif 2 * lower <= period_frames <= 2 * upper:
        relation = "GROUND_TRUTH_REFERENCE_PERIOD_WITHIN_DOUBLED_MEASUREMENT_INTERVAL"
    else:
        relation = "NO_GROUND_TRUTH_REFERENCE_PERIOD_CORRESPONDENCE"
    comparisons.append(
        {
            "common_period_id": candidate["common_period_id"],
            "frozen_period_seconds": candidate["period_seconds"],
            "frozen_corresponding_rate": candidate["corresponding_rate"],
            "relation": relation,
            "candidate_changed": False,
            "metric_role_reassigned": False,
        }
    )

output = {
    "experiment_id": blind["experiment_id"],
    "blind_result_sha256_verified": BLIND_SHA256,
    "blind_freeze_sha256_verified": FREEZE_SHA256,
    "blind_scientific_fingerprint": blind["scientific_fingerprint"],
    "ground_truth": {
        "identity": ground_truth_record["ground_truth_id"],
        "record_sha256": GROUND_TRUTH_SHA256,
        "tempo_rate": str(rate),
        "tempo_beat_unit": ground_truth_record["tempo"]["beat_unit"],
        "reference_period_seconds": str(period),
        "reference_period_frames": str(period_frames),
    },
    "comparisons": comparisons,
    "blind_consensus_classification_unchanged": blind["consensus_classification"],
    "metric_reference_role_scientifically_justified_blindly": False,
    "autonomous_bpm_status": "PARTIAL",
    "ground_truth_used_for_discovery": False,
    "blind_result_modified": False,
}
(RUN_DIR / "post_freeze_validation.json").write_text(
    json.dumps(output, indent=2, sort_keys=True) + "\n"
)
