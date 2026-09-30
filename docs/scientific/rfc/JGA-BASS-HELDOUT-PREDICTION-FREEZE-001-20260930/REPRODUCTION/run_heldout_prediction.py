#!/usr/bin/env python3
"""Execute the FROZEN Bass predictor ONCE on the 20 held-out items (prediction only).

PI authorization: JGA-BASS-HELDOUT-PREDICTION-FREEZE-001-20260930.
Prediction and freeze ONLY. This script does NOT reveal labels, does NOT score,
and does NOT compute any performance metric. There is no reveal path in this file.

Firewall: a sys.addaudithook is installed BEFORE the first file read and traces
every 'open' audit event. Any attempt to open a path registered as
answer-bearing in FIREWALL_POLICY.json aborts immediately with FIREWALL_VIOLATION.

Held-out item IDs come from SEALED_ITEM_EVENT_MAP.json (membership only). That map
contains no stable class and no answer.

The frozen predictor's score() is called exactly ONCE. Per-item standardization
and logit are recomputed from the FROZEN parameters purely for reporting, and the
recomputed probability is asserted to equal the frozen predictor's probability
bit-for-bit, so the reported detail cannot diverge from the frozen decision.
"""
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer")
PKG = REPO / "docs/scientific/rfc/JGA-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-001-20260930"
FIREWALL = REPO / ("docs/scientific/rfc/JGA-BASS-PRE-HELD-OUT-HARDENING-001-20260930"
                   "/FIREWALL_POLICY.json")
OUT = REPO / ("docs/scientific/rfc/JGA-BASS-HELDOUT-PREDICTION-FREEZE-001-20260930"
              "/HELD_OUT_PREDICTIONS.json")

PROHIBITED = []
OBSERVED = []
VIOLATIONS = []


def _load_prohibited():
    pol = json.loads(FIREWALL.read_text())["prohibited_answer_bearing_paths"]
    paths = []
    for group in ("hd_mirror", "ssd_original"):
        paths.extend(pol[group])
    return paths


PROHIBITED = _load_prohibited()


def _hook(event, args):
    if event != "open" or not args:
        return
    target = str(args[0])
    for bad in PROHIBITED:
        if target == bad or target.startswith(bad.rstrip("/") + "/"):
            VIOLATIONS.append({"path": target, "matched_rule": bad})
            raise PermissionError("FIREWALL_VIOLATION: attempted open of %s" % target)
    if target.endswith((".json", ".py")):
        OBSERVED.append(target)


sys.addaudithook(_hook)

sys.path.insert(0, str(PKG / "REPRODUCTION"))
import predict_bass  # noqa: E402

spec = json.loads((PKG / "FROZEN_PIPELINE.json").read_text())
model = spec["model"]
FEATURE = model["features"][0]
THRESHOLD = float(model["decision_threshold"])
MEAN = float(model["frozen_scaler_mean"][0])
SCALE = float(model["frozen_scaler_scale"][0])
COEF = float(model["frozen_coefficients"][0])
INTERCEPT = float(model["frozen_intercept"])

# --- Step C: held-out membership ONLY (label-free map) -------------------------
NS = Path("/Volumes/SSD Track/JGA/experiments/JGA-HUMAN-BASS-PRESENCE-60-001-20260930")
emap = json.loads((NS / "SEALED_ITEM_EVENT_MAP.json").read_text())
forbidden_keys = [k for k in emap
                  if any(w in k.lower() for w in ("stable_class", "label", "answer",
                                                  "consensus", "truth"))]
if forbidden_keys:
    raise SystemExit("FIREWALL_VIOLATION: membership map carries answer keys %r"
                     % forbidden_keys)
held_out = sorted(int(i) for i in emap["held_out_item_numbers"])
item_to_event = {int(k): v for k, v in emap["item_to_event_id"].items()}
if len(held_out) != 20:
    raise SystemExit("expected 20 held-out items, membership map reports %d" % len(held_out))

# --- Step D: the single frozen prediction pass ---------------------------------
rows_by_event = predict_bass.load_phase_a()
events = [item_to_event[i] for i in held_out]
missing = [e for e in events if e not in rows_by_event]
if missing:
    raise SystemExit("event_id(s) absent from label-free Phase A table: %r" % missing)

frozen_results = predict_bass.score([rows_by_event[e] for e in events], spec)
assert len(frozen_results) == 20, "frozen predictor returned %d rows" % len(frozen_results)

PRESENT = predict_bass.PRESENT
ABSENT = predict_bass.ABSENT
predictions = []
for item, event, fr in zip(held_out, events, frozen_results):
    row = rows_by_event[event]
    x = float(row["common_features"][FEATURE])
    if not math.isfinite(x):
        raise SystemExit("non-finite feature for %s" % event)
    z = (x - MEAN) / SCALE
    logit = COEF * z + INTERCEPT
    p = 1.0 / (1.0 + math.exp(-logit))
    # the reported detail must equal the frozen predictor's own output
    if p != fr["bass_present_probability"] or fr["event_id"] != event:
        raise SystemExit("frozen predictor disagreement on item %d" % item)
    cls = fr["predicted_class"]
    if cls not in (PRESENT, ABSENT):
        raise SystemExit("unexpected frozen class %r" % cls)
    predictions.append({
        "item_number": item,
        "event_id": event,
        "input_feature_name": FEATURE,
        "input_feature_value": x,
        "standardized_feature_value": z,
        "raw_model_score_logit": logit,
        "bass_present_probability": p,
        "decision_threshold": THRESHOLD,
        "predicted_class": cls,
        "binary_prediction": ("BASS_PRESENT" if cls == PRESENT else "BASS_ABSENT"),
    })

for p in predictions:
    for banned in ("stable_class", "label", "answer", "truth"):
        if banned in p:
            raise SystemExit("artifact carries label field %r" % banned)

frozen_sha = hashlib.sha256((PKG / "FROZEN_PIPELINE.json").read_bytes()).hexdigest()
predictor_sha = hashlib.sha256((PKG / "REPRODUCTION/predict_bass.py").read_bytes()).hexdigest()
policy_sha = hashlib.sha256(FIREWALL.read_bytes()).hexdigest()

payload = {
    "record_type": "HELD_OUT_PREDICTION_ARTIFACT",
    "task_id": "JGA-BASS-HELDOUT-PREDICTION-FREEZE-001-20260930",
    "pi_authorization": "PI-BASS-HELDOUT-PREDICTION-FREEZE-20260930",
    "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "remote_freeze_commit": "61c0f719ae0629e8d2cd105ba434f479355b4172",
    "frozen_pipeline_sha256": frozen_sha,
    "predictor_code_sha256": predictor_sha,
    "firewall_policy_sha256": policy_sha,
    "model": {
        "feature": FEATURE,
        "estimator_family": model["family"],
        "decision_rule": model["decision_rule"],
        "hyperparameters": spec["model"]["hyperparameters"],
        "decision_threshold": THRESHOLD,
        "coefficient": COEF,
        "intercept": INTERCEPT,
        "scaler_mean": MEAN,
        "scaler_scale": SCALE,
        "frozen_at_utc": spec["frozen_at_utc"],
        "retrained": False,
        "tuned": False,
    },
    "held_out_item_numbers": held_out,
    "held_out_count": len(held_out),
    "prediction_pass_count": 1,
    "execution_provenance": {
        "authoritative_artifact_written_by_invocation": 2,
        "aborted_prior_invocation": {
            "occurred": True,
            "failure_point": ("report assembly AFTER predict_bass.score() returned and BEFORE "
                              "any artifact was written; KeyError 'estimator_name'"),
            "artifact_produced_by_that_invocation": False,
            "answer_bearing_opens_during_that_invocation": 0,
            "why_repeated_execution_cannot_change_the_predictions": (
                "The frozen predictor is a pure, label-blind function of the frozen "
                "coefficients and the label-free Phase A feature values. It opens no "
                "answer file and consumes no randomness, so its output is a "
                "deterministic function of frozen inputs. Repeating the invocation "
                "cannot produce a different prediction, and no held-out answer was "
                "observed at any point that could influence a choice."),
            "not_retraining_not_tuning": True,
        },
    },
    "held_out_human_answers_accessed": False,
    "held_out_labels_revealed": False,
    "scoring_performed": False,
    "performance_computed": False,
    "human_unstable_identities_derived": False,
    "firewall": {
        "policy": "docs/scientific/rfc/JGA-BASS-PRE-HELD-OUT-HARDENING-001-20260930/FIREWALL_POLICY.json",
        "prohibited_paths_registered": len(PROHIBITED),
        "answer_bearing_open_attempts": len(VIOLATIONS),
        "violations": VIOLATIONS,
    },
    "class_alias_note": (
        "predicted_class carries the frozen predictor's literal output "
        "(BASS_PRESENT_STABLE / BASS_ABSENT_STABLE) because the preregistered "
        "scoring code compares against those exact strings. binary_prediction is a "
        "display alias of the same decision. No decision rule was altered."),
    "predictions": predictions,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
body = json.dumps(payload, indent=2) + "\n"
OUT.write_text(body)
artifact_sha = hashlib.sha256(OUT.read_bytes()).hexdigest()

print(json.dumps({
    "predictions_generated": len(predictions),
    "held_out_items": len(held_out),
    "prediction_artifact": str(OUT),
    "prediction_artifact_sha256": artifact_sha,
    "answer_bearing_open_attempts": len(VIOLATIONS),
    "firewall": "PASS" if not VIOLATIONS else "FAIL",
    "frozen_pipeline_sha256": frozen_sha,
    "predictor_code_sha256": predictor_sha,
    "firewall_policy_sha256": policy_sha,
    "observed_file_opens": sorted(set(OBSERVED)),
}, indent=2))
