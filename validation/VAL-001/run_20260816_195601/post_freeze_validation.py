"""Post-freeze validation only; Ground Truth never participates in discovery."""

import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
BLIND_SHA = "0a5ab86f1c6c30d9e389c8e1c47a9689deb7eef7db0fc7b13ee189f95ee96045"
FREEZE_SHA = "255a1b481ca537891a91c77913d13b4b56d497c6f20053358bb47df3979e3f51"
GT_SHA = "9f219660d933b9084190708b8b7ae9ef092c987aff767390750351e83a93090d"

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

blind_path, freeze_path = RUN / "blind_result.json", RUN / "blind_freeze.json"
gt_path = ROOT / "validation/VAL-001/run_20260809_065633/baseline.json"
if (sha(blind_path), sha(freeze_path), sha(gt_path)) != (BLIND_SHA, FREEZE_SHA, GT_SHA):
    raise RuntimeError("freeze or Ground Truth identity mismatch")
blind = json.loads(blind_path.read_text())
gt = json.loads(gt_path.read_text())["ground_truth"]
rate = Decimal(gt["tempo"]["beats_per_minute"])
output = {
    "experiment_id": blind["experiment_id"],
    "blind_result_sha256_verified": BLIND_SHA,
    "blind_freeze_sha256_verified": FREEZE_SHA,
    "blind_classification_unchanged": blind["blind_classification"],
    "ground_truth": {"identity": gt["ground_truth_id"], "record_sha256": GT_SHA,
                     "tempo_rate": str(rate), "beat_unit": gt["tempo"]["beat_unit"]},
    "blind_selected_authoritative_family": "UNRESOLVED",
    "strength_resolved_hierarchy": False,
    "autonomous_bpm_status": "PARTIAL",
    "production_implementation_justified": False,
    "ground_truth_used_for_discovery": False,
}
(RUN / "post_freeze_validation.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
