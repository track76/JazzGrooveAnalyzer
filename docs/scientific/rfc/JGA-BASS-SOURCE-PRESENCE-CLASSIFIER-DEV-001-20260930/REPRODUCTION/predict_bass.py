#!/usr/bin/env python3
"""Score FullMix landmarks with the FROZEN Bass source-presence pipeline.

Loads FROZEN_PIPELINE.json and returns, for each requested landmark:
  - bass_present_probability
  - predicted_class  (BASS_PRESENT_STABLE / BASS_ABSENT_STABLE)

This script NEVER reads human labels. It is deliberately label-blind so that it
cannot be used to open held-out answers. It reads only the frozen record and the
Phase A feature table.

No uncertainty or confidence value is returned: the frozen scores are uncalibrated
margins from a 32-row development fit and must not be read as confidence.

    <python> predict_bass.py --events IDN_F000091,IDN_F000092
    <python> predict_bass.py --from-items 1,2,3
"""
import argparse
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
FROZEN = PKG / "FROZEN_PIPELINE.json"
PA = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/"
          "JGA-FULLMIX-INSTRUMENT-IDENTITY-001-20260929")
NS = Path("/Volumes/SSD Track/JGA/experiments/JGA-HUMAN-BASS-PRESENCE-60-001-20260930")
PRESENT = "BASS_PRESENT_STABLE"
ABSENT = "BASS_ABSENT_STABLE"


def load_phase_a():
    return {r["event_id"]: r
            for r in json.loads((PA / "PHASE_A/SOURCE_EVIDENCE_TABLE.json").read_text())["rows"]}


def score(records, spec=None):
    """Score an iterable of Phase A rows. Returns list of dicts."""
    spec = spec or json.loads(FROZEN.read_text())
    feats = spec["model"]["features"]
    thr = spec["model"]["decision_threshold"]
    mean = np.array(spec["model"]["frozen_scaler_mean"], float)
    scale = np.array(spec["model"]["frozen_scaler_scale"], float)
    coef = np.array(spec["model"]["frozen_coefficients"], float)
    b0 = float(spec["model"]["frozen_intercept"])
    out = []
    for r in records:
        v = np.array([float(r["common_features"][f]) for f in feats], float)
        if not np.all(np.isfinite(v)):
            raise ValueError("non-finite feature for %s; the frozen record declares no "
                             "imputation for missing values" % r.get("event_id"))
        z = (v - mean) / scale
        p = 1.0 / (1.0 + np.exp(-(float(z @ coef) + b0)))
        out.append({
            "event_id": r["event_id"],
            "bass_present_probability": float(p),
            "predicted_class": PRESENT if p >= thr else ABSENT,
            "decision_threshold": thr,
        })
    return out


def main():
    ap = argparse.ArgumentParser(description="Score landmarks with the frozen Bass pipeline")
    ap.add_argument("--events", help="comma-separated Phase A event_ids")
    ap.add_argument("--from-items", help="comma-separated dataset item numbers (uses the "
                                          "frozen item->event map, membership only)")
    ap.add_argument("--json-out", help="write results to this path")
    a = ap.parse_args()
    spec = json.loads(FROZEN.read_text())
    rows = load_phase_a()
    if a.events:
        want = [e.strip() for e in a.events.split(",") if e.strip()]
    elif a.from_items:
        emap = json.loads((NS / "SEALED_ITEM_EVENT_MAP.json").read_text())
        i2e = {int(k): v for k, v in emap["item_to_event_id"].items()}
        want = [i2e[int(i)] for i in a.from_items.split(",") if i.strip()]
    else:
        ap.error("give --events or --from-items")
    missing = [e for e in want if e not in rows]
    if missing:
        raise SystemExit("unknown event_id(s): %s" % missing)
    res = score([rows[e] for e in want], spec)
    for r in res:
        print("%-14s p=%.4f  %s" % (r["event_id"], r["bass_present_probability"],
                                    r["predicted_class"]))
    if a.json_out:
        payload = {
            "task_id": spec["task_id"],
            "pipeline_status": spec["status"],
            "held_out_human_answers_accessed": False,
            "uncertainty_provided": False,
            "results": res,
        }
        Path(a.json_out).write_text(json.dumps(payload, indent=2) + "\n")
        print("wrote %s" % a.json_out)


if __name__ == "__main__":
    main()
