#!/usr/bin/env python3
"""Rehearsal of the future held-out prediction-freeze sequence (steps A-K).

THIS TASK EXECUTES ONLY A-I WITH DUMMY, NON-HELD-OUT DATA.

Steps J (open human held-out labels) and K (score) are demonstrated as REFUSED
gates only. They are never executed here: doing so requires separate PI
authorization. No real held-out item number, prediction or label is used.

The sequence exists to make "prediction frozen before reveal" mechanically
auditable rather than merely asserted in prose.

    <python> rehearse_freeze_sequence.py --work-dir /tmp/rehearsal
"""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
REPO = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer")

DUMMY_ITEMS = ["DUMMY_ITEM_%02d" % i for i in range(1, 21)]  # 20 dummies, not item numbers


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    try:
        return subprocess.run(["git", "-C", str(REPO)] + list(args),
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "UNKNOWN"


def step_a_verify_model_anchor(anchor_path):
    """A. verify the frozen-anchor fingerprint covers the live package."""
    anchor = json.loads(Path(anchor_path).read_text())
    root = REPO / anchor["package_path"]
    mismatches, checked = [], 0
    for entry in anchor["files"]:
        f = root / entry["path"]
        if not f.exists():
            mismatches.append("%s MISSING" % entry["path"])
            continue
        if sha256_file(f) != entry["sha256"]:
            mismatches.append("%s HASH MISMATCH" % entry["path"])
        checked += 1
    return {"step": "A_verify_model_anchor", "files_checked": checked,
            "mismatches": mismatches, "passed": not mismatches}


def step_b_load_predictor():
    """B. load the frozen predictor (no data read yet)."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(HERE))
    import predict_bass
    spec = json.loads(predict_bass.FROZEN.read_text())
    doc = spec.get("threshold_documentation", {})
    return {"step": "B_load_predictor",
            "operative_decision_threshold": spec["model"]["decision_threshold"],
            "feature": spec["model"]["features"][0],
            "non_operative_in_fold_mode_ignored":
                doc.get("in_fold_threshold_mode_NOT_the_frozen_threshold")}


def step_c_identify_by_membership_only():
    """C. identify target item IDs using MEMBERSHIP ONLY.

    In the real run this reads SEALED_ITEM_EVENT_MAP.json (label-free).
    The rehearsal uses dummy identifiers and reads no membership file at all.
    """
    return {"step": "C_identify_membership_only",
            "n_items": len(DUMMY_ITEMS),
            "source": "DUMMY (rehearsal; real run reads label-free SEALED_ITEM_EVENT_MAP.json)",
            "labels_read": False,
            "items": list(DUMMY_ITEMS)}


def step_d_generate_predictions():
    """D. generate 20 predictions WITHOUT any answer access, on synthetic features."""
    sys.path.insert(0, str(HERE))
    import predict_bass
    spec = json.loads(predict_bass.FROZEN.read_text())
    feats = spec["model"]["features"]
    records = [{"event_id": it, "common_features": dict((f, 30.0 + 7.0 * i) for f in feats)}
               for i, it in enumerate(DUMMY_ITEMS)]
    rows = predict_bass.score(records, spec)
    results = []
    for it, r in zip(DUMMY_ITEMS, rows):
        results.append({"item_number": it, "event_id": r["event_id"],
                        "bass_present_probability": r["bass_present_probability"],
                        "predicted_class": r["predicted_class"],
                        "decision_threshold": r["decision_threshold"]})
    return {"step": "D_generate_predictions", "n": len(results),
            "human_answers_accessed": False, "results": results}


def step_e_write_prediction_artifact(results, work):
    """E. write the prediction artifact."""
    art = work / "HELD_OUT_PREDICTIONS.json"
    art.write_text(json.dumps(
        {"task_id": "REHEARSAL_DUMMY_NOT_HELD_OUT", "is_rehearsal_dummy_data": True,
         "held_out_human_answers_accessed": False, "results": results},
        indent=2, sort_keys=True) + "\n")
    return {"step": "E_write_prediction_artifact", "path": str(art)}


def step_f_hash_artifact(art):
    """F. hash the prediction artifact."""
    return {"step": "F_hash_prediction_artifact", "sha256": sha256_file(art)}


def step_g_prediction_freeze_record(art, pred_hash, anchor_hash, out):
    """G. externally backed PREDICTION_FREEZE record."""
    rec = {
        "record_type": "PREDICTION_FREEZE",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "git_head": git("rev-parse", "HEAD"),
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "model_anchor_sha256": anchor_hash,
        "prediction_artifact_path": str(art),
        "prediction_artifact_sha256": pred_hash,
        "n_predictions": 20,
        "exact_item_ids": list(DUMMY_ITEMS),
        "held_out_human_answers_accessed": False,
        "authoritative": "REHEARSAL_DUMMY_DATA_NOT_A_HELD_OUT_FREEZE",
    }
    rec["record_sha256"] = hashlib.sha256(
        json.dumps(rec, sort_keys=True).encode()).hexdigest()
    out.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    return {"step": "G_prediction_freeze_record", "path": str(out),
            "record_sha256": rec["record_sha256"]}


def step_h_close_prediction_writer_authority():
    """H. close prediction writer authority."""
    return {"step": "H_close_prediction_writer_authority",
            "prediction_writer_authority": "CLOSED",
            "further_prediction_edits_require": "separate PI authorization"}


def step_i_verify_artifact_unchanged(art, pred_hash):
    """I. independently verify the prediction artifact is unchanged."""
    now = sha256_file(art)
    return {"step": "I_verify_artifact_unchanged", "recorded": pred_hash,
            "observed": now, "passed": now == pred_hash}


def step_j_reveal_gate_blocked():
    """J. REFUSED in this task: opening human held-out labels."""
    return {"step": "J_reveal", "executed": False,
            "reason": "REQUIRES SEPARATE PI AUTHORIZATION AFTER PREDICTION FREEZE",
            "would_open": "held-out human label artifacts on the HD mirror"}


def step_k_score_gate_blocked():
    """K. REFUSED in this task: scoring the real held-out set."""
    return {"step": "K_score", "executed": False,
            "reason": "REQUIRES SEPARATE PI AUTHORIZATION AFTER REVEAL",
            "scoring_code_frozen": str(HERE / "score_bass_heldout.py")}


def rehearse(anchor_path, work):
    work = Path(work)
    work.mkdir(parents=True, exist_ok=True)
    a = step_a_verify_model_anchor(anchor_path)
    b = step_b_load_predictor()
    c = step_c_identify_by_membership_only()
    d = step_d_generate_predictions()
    e = step_e_write_prediction_artifact(d["results"], work)
    f = step_f_hash_artifact(e["path"])
    g = step_g_prediction_freeze_record(
        e["path"], f["sha256"], sha256_file(anchor_path), work / "PREDICTION_FREEZE.json")
    h = step_h_close_prediction_writer_authority()
    i = step_i_verify_artifact_unchanged(e["path"], f["sha256"])
    j = step_j_reveal_gate_blocked()
    k = step_k_score_gate_blocked()
    return {"rehearsal": True, "dummy_data_only": True,
            "real_held_out_answers_accessed": False,
            "real_held_out_predictions_generated": False,
            "steps": [a, b, c, d, e, f, g, h, i, j, k],
            "sequence_order_verified": [s["step"][0] for s in (a, b, c, d, e, f, g, h, i, j, k)],
            "all_executable_steps_passed": a["passed"] and i["passed"],
            "blocked_gates": [j["step"], k["step"]]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Rehearse the prediction-freeze sequence on dummy data")
    ap.add_argument("--model-anchor", required=True)
    ap.add_argument("--work-dir", default="/tmp/jga_bass_freeze_rehearsal")
    ap.add_argument("--json-out")
    ns = ap.parse_args()
    r = rehearse(ns.model_anchor, ns.work_dir)
    print(json.dumps(r, indent=2, sort_keys=True))
    if ns.json_out:
        Path(ns.json_out).write_text(json.dumps(r, indent=2, sort_keys=True) + "\n")
