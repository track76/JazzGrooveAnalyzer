#!/usr/bin/env python3
"""PREREGISTERED held-out scoring implementation for the frozen Bass classifier.

This module is FROZEN BEFORE any held-out prediction or reveal. It is written and
tested now, on synthetic fixtures only, so that the metric definitions cannot
become post-hoc once results are known.

Design constraints (PI authorization JGA-BASS-PRE-HELD-OUT-HARDENING-001-20260930):
  * human-unstable cases are SEPARATED, never counted as binary errors;
  * only the preregistered metric set is computed;
  * predictions are NEVER altered;
  * labels are NEVER altered, relabelled or dropped;
  * output is deterministic and sorted;
  * no categorical performance boundary is produced.

It reads a frozen prediction artifact and, ONLY AFTER separate PI reveal
authorization, a human label file. It contains no model and no retraining path.

    <python> score_bass_heldout.py --predictions P.json --labels L.json
"""
import argparse
import json
import math
from pathlib import Path

PRESENT = "BASS_PRESENT_STABLE"
ABSENT = "BASS_ABSENT_STABLE"
UNSTABLE = "BASS_HUMAN_UNSTABLE"

# The preregistered metric set. Nothing outside this list is reported as
# performance, and no categorical verdict may be derived from it.
PREREGISTERED_METRICS = ("balanced_accuracy", "sensitivity_bass_present",
                         "specificity_bass_absent", "precision_bass_present",
                         "f1_bass_present", "confusion_matrix")

CATEGORICAL_BOUNDARY_AUTHORIZED = False
SMALL_N_CAVEAT = (
    "n is too small for a defensible categorical performance boundary. "
    "No strong/partial/failure threshold is authorized.")


def _clopper_pearson(k, n, alpha=0.05):
    """Exact binomial confidence interval. Returns (lo, hi); (nan, nan) if n == 0."""
    if n <= 0:
        return float("nan"), float("nan")
    try:
        from scipy.stats import beta
        lo = 0.0 if k == 0 else beta.ppf(alpha / 2.0, k, n - k + 1)
        hi = 1.0 if k == n else beta.ppf(1.0 - alpha / 2.0, k + 1, n - k)
    except Exception:
        lo = hi = float("nan")
    return float(lo), float(hi)


def separate_unstable(labels_by_item):
    """Split human labels into the stable binary set and the unstable set.

    Unstable cases are reported separately and are NEVER relabelled into the
    binary set, never silently dropped, and never counted as binary errors.
    """
    stable, unstable = [], []
    for item in sorted(labels_by_item):
        cls = labels_by_item[item]
        if cls == UNSTABLE:
            unstable.append(item)
        elif cls in (PRESENT, ABSENT):
            stable.append(item)
        else:
            raise ValueError("unexpected stable_class for item %r: %r" % (item, cls))
    return stable, unstable


def _confusion(pairs):
    tp = sum(1 for _, y, p in pairs if y == 1 and p == 1)
    tn = sum(1 for _, y, p in pairs if y == 0 and p == 0)
    fp = sum(1 for _, y, p in pairs if y == 0 and p == 1)
    fn = sum(1 for _, y, p in pairs if y == 1 and p == 0)
    return {"tn": tn, "fp": fp, "fn": fn, "tp": tp}


def compute_metrics(pairs):
    """pairs = [(item_number, y_true_int, y_pred_int)] over STABLE items only."""
    c = _confusion(pairs)
    tp, tn, fp, fn = c["tp"], c["tn"], c["fp"], c["fn"]
    sens_den, spec_den, prec_den = tp + fn, tn + fp, tp + fp
    sens = tp / sens_den if sens_den else float("nan")
    spec = tn / spec_den if spec_den else float("nan")
    prec = tp / prec_den if prec_den else float("nan")
    f1 = (2 * prec * sens / (prec + sens)) if (prec_den and sens_den
                                               and not math.isnan(prec)
                                               and not math.isnan(sens)
                                               and (prec + sens) > 0) else 0.0
    ba = (sens + spec) / 2 if not (math.isnan(sens) or math.isnan(spec)) else float("nan")
    lo_s, hi_s = _clopper_pearson(tp, sens_den)
    lo_p, hi_p = _clopper_pearson(tp, prec_den)
    lo_c, hi_c = _clopper_pearson(tn, spec_den)
    return {
        "balanced_accuracy": ba,
        "sensitivity_bass_present": sens,
        "specificity_bass_absent": spec,
        "precision_bass_present": prec,
        "f1_bass_present": f1,
        "confusion_matrix": c,
        "exact_intervals_95_clopper_pearson": {
            "sensitivity_bass_present": [lo_s, hi_s],
            "specificity_bass_absent": [lo_c, hi_c],
            "precision_bass_present": [lo_p, hi_p],
        },
        "denominators": {"n_stable_scored": len(pairs),
                         "sensitivity_denominator_present": sens_den,
                         "specificity_denominator_absent": spec_den,
                         "precision_denominator_predicted_present": prec_den},
        "balanced_accuracy_interval": None,
        "balanced_accuracy_interval_note": (
            "NOT PROVIDED. Balanced accuracy is a ratio of two proportions on this "
            "single small sample; a binomial interval would not be valid."),
        "small_n_caveat": SMALL_N_CAVEAT,
        "categorical_boundary_authorized": CATEGORICAL_BOUNDARY_AUTHORIZED,
    }


def score(predictions, labels):
    """Score a frozen prediction artifact against revealed human labels.

    predictions: [{"item_number", "event_id", "bass_present_probability",
                   "predicted_class", "decision_threshold"}]
    labels:      [{"item_number", "stable_class"}]

    Neither argument is mutated. The prediction artifact must not carry labels.
    """
    labels_by_item = {int(r["item_number"]): r["stable_class"] for r in labels}
    pred_by_item = {}
    for r in predictions:
        if any(k in r for k in ("stable_class", "label", "answer", "truth")):
            raise ValueError("prediction artifact carries a label field: %r"
                             % sorted(set(r) & {"stable_class", "label", "answer", "truth"}))
        pred_by_item[int(r["item_number"])] = r

    stable, unstable = separate_unstable(labels_by_item)

    scored, missing = [], []
    for item in stable:
        if item not in pred_by_item:
            missing.append(item)
            continue
        cls = pred_by_item[item]["predicted_class"]
        if cls not in (PRESENT, ABSENT):
            raise ValueError("unexpected predicted_class for item %r: %r" % (item, cls))
        scored.append((item, 1 if labels_by_item[item] == PRESENT else 0,
                       1 if cls == PRESENT else 0))

    if missing:
        raise ValueError("no frozen prediction for stable item(s): %r" % sorted(missing))

    metrics = compute_metrics(scored)
    return {
        "preregistered_metrics": list(PREREGISTERED_METRICS),
        "counts": {
            "stable_present": sum(1 for i in stable if labels_by_item[i] == PRESENT),
            "stable_absent": sum(1 for i in stable if labels_by_item[i] == ABSENT),
            "human_unstable": len(unstable),
            "stable_total": len(stable),
            "scored": len(scored),
        },
        "human_unstable_items_reported_separately": len(unstable),
        "human_unstable_handling": (
            "Excluded from binary scoring by preregistration. NOT counted as binary "
            "errors. NOT relabelled. Reported as an aggregate count only."),
        "unstable_item_identities_disclosed": False,
        "metrics": metrics,
        "post_reveal_prohibitions": POST_REVEAL_PROHIBITIONS,
        "categorical_performance_verdict": None,
        "categorical_verdict_note": (
            "WITHHELD BY PREREGISTRATION. No strong/partial/failure boundary is "
            "authorized for this held-out sample size."),
        "deterministic": True,
    }


POST_REVEAL_PROHIBITIONS = [
    "NO threshold adjustment based on held-out results.",
    "NO feature replacement.",
    "NO model selection.",
    "NO relabelling of stable human answers.",
    "NO deletion of stable cases.",
    "NO second attempt on this held-out set.",
    "Any future classifier improvement must be a NEW development cycle; this "
    "held-out result remains historical evidence and cannot be reused as if it "
    "were a fresh evaluation set.",
]


def main():
    ap = argparse.ArgumentParser(description="Preregistered held-out scoring")
    ap.add_argument("--predictions", required=True, help="frozen prediction artifact")
    ap.add_argument("--labels", required=True,
                    help="revealed human label file (post-reveal only)")
    ap.add_argument("--json-out")
    a = ap.parse_args()
    preds = json.loads(Path(a.predictions).read_text())
    labels = json.loads(Path(a.labels).read_text())
    preds = preds["results"] if isinstance(preds, dict) else preds
    labels = labels["items"] if isinstance(labels, dict) else labels
    out = score(preds, labels)
    print(json.dumps(out, indent=2, sort_keys=True))
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
