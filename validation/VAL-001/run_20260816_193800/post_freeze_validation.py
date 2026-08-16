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
BLIND_SHA256 = "c674a2b9ddd9831b9babbdaf9e01b659c1ca044e5d90928bd5a7ee149eb7eda0"
FREEZE_SHA256 = "6feaf58a1ae05273d4b95dfb9b6149e896f0b4f8b38c0466ba628891f891284a"
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

measurements = {
    measurement["common_period_id"]: measurement
    for source in blind["source_results"].values()
    for measurement in source["measurements"]
}
family_relations = {}
for family, candidate_ids in blind["candidate_families"].items():
    relations = []
    for candidate_id in candidate_ids:
        lower, upper = (
            Decimal(str(v))
            for v in measurements[candidate_id]["measurement_interval_frames"]
        )
        relations.append(lower <= period_frames <= upper)
    family_relations[family] = {
        "contains_authoritative_reference_period": any(relations),
        "candidate_relations": relations,
    }

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
    "family_relations": family_relations,
    "blind_classification_unchanged": blind["blind_final_classification"],
    "selected_authoritative_family_blindly": "UNRESOLVED",
    "metric_reference_role_scientifically_justified": False,
    "autonomous_bpm_status": "PARTIAL",
    "production_implementation_justified": False,
    "ground_truth_used_for_discovery": False,
    "blind_result_modified": False,
}
(RUN_DIR / "post_freeze_validation.json").write_text(
    json.dumps(output, indent=2, sort_keys=True) + "\n"
)
