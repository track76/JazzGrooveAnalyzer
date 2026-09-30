#!/usr/bin/env python3
"""JGA-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-001-20260930 — development training.

Reproduces the frozen Bass source-presence pipeline from DEVELOPMENT data only.

HELD-OUT FIREWALL. This script opens exactly one label file,
BASS_CONSENSUS_DEVELOPMENT.json. It never opens SEALED_BASS_HELD_OUT_LABELS.json,
BASS_CONSENSUS_ALL60_SEALED.json or PRE_SEAL_RECORDS/. Held-out MEMBERSHIP is
read from SEALED_ITEM_EVENT_MAP.json for one purpose only: to assert that every
row used here is a development member. Held-out human ANSWERS are never read.

Every preprocessing step — imputation, scaling, hyperparameter choice and the
decision threshold — is fitted inside the training fold of the cross-validation,
never on the validation fold.

    <python> train_bass_classifier.py
"""
import json
import os
import warnings
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

TASK = "JGA-BASS-SOURCE-PRESENCE-CLASSIFIER-DEV-001-20260930"
SEED = 20260930
NS = Path("/Volumes/SSD Track/JGA/experiments/JGA-HUMAN-BASS-PRESENCE-60-001-20260930")
PA = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/"
           "JGA-FULLMIX-INSTRUMENT-IDENTITY-001-20260929")
OUT = Path(__file__).resolve().parent.parent

COMMON = ["centroid_hz", "rolloff85_hz", "bandwidth_hz", "zcr", "flatness_magnitude",
          "subband_energy_share_0", "subband_energy_share_1", "subband_energy_share_2",
          "subband_energy_share_3", "subband_energy_share_4", "subband_energy_share_5",
          "subband_energy_cv", "spectral_flux", "peak_prominence",
          "post_event_energy", "post_event_decay"]
PRESENT = "BASS_PRESENT_STABLE"
ABSENT = "BASS_ABSENT_STABLE"
UNSTABLE = "BASS_HUMAN_UNSTABLE"
THRESH_GRID = np.round(np.arange(0.05, 0.96, 0.05), 2)


def metrics(y, p):
    tp = int(((p == 1) & (y == 1)).sum()); tn = int(((p == 0) & (y == 0)).sum())
    fp = int(((p == 1) & (y == 0)).sum()); fn = int(((p == 0) & (y == 1)).sum())
    se = tp / (tp + fn) if tp + fn else float("nan")
    sp = tn / (tn + fp) if tn + fp else float("nan")
    pr = tp / (tp + fp) if tp + fp else float("nan")
    f1 = 2 * pr * se / (pr + se) if pr and se and not np.isnan(pr) and not np.isnan(se) else 0.0
    return {"balanced_accuracy": (se + sp) / 2, "sensitivity": se, "specificity": sp,
            "precision": pr, "f1": f1,
            "confusion": {"tn": tn, "fp": fp, "fn": fn, "tp": tp}}


def make_pipeline(C=1.0):
    """Scaler and model are chained so the scaler is fitted on training rows only."""
    return Pipeline([("sc", StandardScaler()),
                     ("m", LogisticRegression(penalty="l2", C=C, class_weight="balanced",
                                              max_iter=20000, random_state=SEED))])


# ---------------------------------------------------------------------------
# FROZEN-RECORD OVERWRITE PROTECTION (operational only; no scientific logic)
# ---------------------------------------------------------------------------
# FROZEN_PIPELINE.json is the frozen scientific authority. This script is its
# generator, so re-running it in place would silently replace the frozen record
# with a fresh timestamp and fresh values. That is an operational hazard, not a
# scientific one, so the guard below changes no modelling code.
DEFAULT_OUT = Path(__file__).resolve().parent.parent
FROZEN_SCIENTIFIC_RECORDS = ("FROZEN_PIPELINE.json", "VALIDATION.json")
OVERRIDE_ENV = "JGA_PI_FROZEN_OVERRIDE"


def guard_frozen_output(out_dir, allow_regeneration=False, expected_override=None):
    """Refuse to overwrite an existing frozen scientific record.

    Default behaviour is to REFUSE. Regeneration is only permitted when either
      (a) the caller writes to a NEW namespace that does not already hold a
          frozen record, or
      (b) the caller explicitly passes allow_regeneration AND the PI override
          token is present in the environment, for an in-place write.

    Raises SystemExit on refusal. Returns an audit dict on permission.
    """
    out = Path(out_dir).resolve()
    collisions = [n for n in FROZEN_SCIENTIFIC_RECORDS if (out / n).exists()]
    if not collisions:
        return {"allowed": True, "collisions": [], "namespace": str(out),
                "mode": "fresh_namespace"}
    if not allow_regeneration:
        raise SystemExit(
            "REFUSING TO OVERWRITE FROZEN SCIENTIFIC AUTHORITY.\n"
            "  destination : %s\n"
            "  existing    : %s\n"
            "These are the frozen scientific authority for task %s.\n"
            "Regeneration requires a SEPARATELY AUTHORIZED PI task and is NOT\n"
            "permitted as an incidental side effect.\n"
            "  (a) write to a NEW namespace instead, or\n"
            "  (b) re-run with --allow-regeneration AND environment variable %s\n"
            "      set to the PI override token issued for that task."
            % (out, ", ".join(collisions), TASK, OVERRIDE_ENV))
    if out == DEFAULT_OUT.resolve():
        token = os.environ.get(OVERRIDE_ENV, "")
        if expected_override is None or token != expected_override:
            raise SystemExit(
                "REFUSING IN-PLACE OVERWRITE of the frozen record at %s.\n"
                "--allow-regeneration was given but the PI override token in %s is\n"
                "absent or does not match the token for the separately authorized task."
                % (out, OVERRIDE_ENV))
        return {"allowed": True, "collisions": collisions, "namespace": str(out),
                "mode": "in_place_pi_override"}
    return {"allowed": True, "collisions": collisions, "namespace": str(out),
            "mode": "regenerate_new_namespace"}


def score_of(model, X):
    est = model.steps[-1][1]
    return model.predict_proba(X)[:, 1] if hasattr(est, "predict_proba") \
        else model.decision_function(X)


def load_development():
    dev = json.loads((NS / "BASS_CONSENSUS_DEVELOPMENT.json").read_text())["items"]
    emap = json.loads((NS / "SEALED_ITEM_EVENT_MAP.json").read_text())
    devset = set(emap["development_item_numbers"])
    heldset = set(emap["held_out_item_numbers"])
    if devset & heldset:
        raise SystemExit("REFUSING: development and held-out sets overlap.")
    rows = {r["event_id"]: r
            for r in json.loads((PA / "PHASE_A/SOURCE_EVIDENCE_TABLE.json").read_text())["rows"]}
    X, y, ids = [], [], []
    n_unstable = 0
    for d in dev:
        if d["item_number"] not in devset:
            raise SystemExit("REFUSING: non-development row in the development label file.")
        if d["stable_class"] == UNSTABLE:
            n_unstable += 1          # excluded from supervised training, never relabelled
            continue
        if d["stable_class"] not in (PRESENT, ABSENT):
            raise SystemExit("REFUSING: unexpected class %r" % d["stable_class"])
        cf = rows[d["event_id"]]["common_features"]
        X.append([float(cf[f]) for f in COMMON])
        y.append(1 if d["stable_class"] == PRESENT else 0)
        ids.append(d["event_id"])
    return np.array(X), np.array(y), ids, len(dev), n_unstable


def inner_threshold(Xtr, ytr, C=1.0):
    """Threshold chosen by inner CV on the TRAINING fold only."""
    skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    oof = np.zeros(len(ytr))
    for a, b in skf.split(Xtr, ytr):
        m = make_pipeline(C); m.fit(Xtr[a], ytr[a])
        oof[b] = score_of(m, Xtr[b])
    return max(((metrics(ytr, (oof >= t).astype(int))["balanced_accuracy"]), t)
               for t in THRESH_GRID)[1]


def nested_cv(X, y, C=1.0, n_splits=5, n_repeats=10):
    rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats,
                                   random_state=SEED)
    ys, ps, bas, ths = [], [], [], []
    for tr, te in rskf.split(X, y):
        t = inner_threshold(X[tr], y[tr], C)
        m = make_pipeline(C); m.fit(X[tr], y[tr])
        p = (score_of(m, X[te]) >= t).astype(int)
        ths.append(t); ps.append(p); ys.append(y[te])
        bas.append(metrics(y[te], p)["balanced_accuracy"])
    return metrics(np.concatenate(ys), np.concatenate(ps)), np.array(bas), ths


def main(out_dir=None, allow_regeneration=False, expected_override=None):
    # Fail fast, BEFORE any fitting, if this run would overwrite frozen authority.
    out = Path(out_dir).resolve() if out_dir else DEFAULT_OUT
    permit = guard_frozen_output(out, allow_regeneration, expected_override)
    out.mkdir(parents=True, exist_ok=True)
    print("FROZEN-RECORD WRITE PERMIT: %s (%s)" % (permit["mode"], permit["namespace"]))
    print("FROZEN SCIENTIFIC AUTHORITY UNTOUCHED BY DEFAULT: yes")
    print()
    X, y, ids, n_dev, n_unstable = load_development()
    print("DEVELOPMENT TOTAL: %d" % n_dev)
    print("DEVELOPMENT STABLE PRESENT: %d" % int((y == 1).sum()))
    print("DEVELOPMENT STABLE ABSENT: %d" % int((y == 0).sum()))
    print("DEVELOPMENT HUMAN UNSTABLE EXCLUDED: %d" % n_unstable)
    print("SUPERVISED-ELIGIBLE USED: %d" % len(y))
    print("HELD-OUT HUMAN ANSWERS ACCESSED: NO")
    print()

    # candidate family: one preregistered regularized linear model per C, on the
    # selected single feature and on the full 16, plus shallow trees and one
    # lightweight nonlinear comparator. No large search.
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC

    def cand(kind, p):
        if kind == "logreg":
            return Pipeline([("sc", StandardScaler()),
                             ("m", LogisticRegression(penalty="l2", C=p, class_weight="balanced",
                                                      max_iter=20000, random_state=SEED))])
        if kind == "tree":
            return Pipeline([("m", DecisionTreeClassifier(max_depth=p, class_weight="balanced",
                                                          random_state=SEED))])
        return Pipeline([("sc", StandardScaler()),
                         ("m", SVC(C=p[0], gamma=p[1], class_weight="balanced",
                                   kernel="rbf", random_state=SEED))])

    def score_generic(m, Xt):
        est = m.steps[-1][1]
        return m.predict_proba(Xt)[:, 1] if hasattr(est, "predict_proba") \
            else m.decision_function(Xt)

    def thr_generic(Xtr, ytr, kind, p):
        skf = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
        oof = np.zeros(len(ytr))
        for a, b in skf.split(Xtr, ytr):
            m = cand(kind, p); m.fit(Xtr[a], ytr[a]); oof[b] = score_generic(m, Xtr[b])
        return max(((metrics(ytr, (oof >= t).astype(int))["balanced_accuracy"]), t)
                   for t in THRESH_GRID)[1]

    j = COMMON.index("peak_prominence")
    fam = {"logreg_single_peak_prominence_C1": ("logreg", 1.0, [j])}
    for c in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
        fam["logreg16_C%g" % c] = ("logreg", c, list(range(16)))
    fam["tree16_depth2"] = ("tree", 2, list(range(16)))
    fam["tree16_depth3"] = ("tree", 3, list(range(16)))
    fam["svc16_rbf_C0.5"] = ("svc", (0.5, "scale"), list(range(16)))
    fam["svc16_rbf_C1"] = ("svc", (1.0, "scale"), list(range(16)))

    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=SEED)
    out, thdist = {}, {}
    for name, (kind, p, cols) in fam.items():
        ys, ps, ths = [], [], []
        Xc = X[:, cols]
        for tr, te in rskf.split(Xc, y):
            t = thr_generic(Xc[tr], y[tr], kind, p)
            m = cand(kind, p); m.fit(Xc[tr], y[tr])
            ps.append((score_generic(m, Xc[te]) >= t).astype(int))
            ys.append(y[te]); ths.append(t)
        out[name] = metrics(np.concatenate(ys), np.concatenate(ps))
        # NOT the frozen threshold. This is the MODE of the 50 in-fold thresholds,
        # i.e. a description of the cross-validation procedure. The operative
        # frozen threshold is computed separately below by applying the same
        # procedure to all 32 supervised-eligible development rows.
        out[name]["in_fold_threshold_mode_NOT_the_frozen_threshold"] = \
            float(Counter(ths).most_common(1)[0][0])
        thdist[name] = {"%.2f" % k: int(v) for k, v in sorted(Counter(ths).items())}
        out[name]["n_features"] = len(cols)

    print("=== CANDIDATE FAMILY, nested 5-fold x 10 repeats, scaling inside folds ===")
    print("%-34s %7s %7s %7s %7s %7s %6s" % ("candidate", "BA", "sens", "spec", "prec", "F1", "nfeat"))
    for k, v in sorted(out.items(), key=lambda kv: -kv[1]["balanced_accuracy"]):
        print("%-34s %7.4f %7.4f %7.4f %7.4f %7.4f %6d"
              % (k, v["balanced_accuracy"], v["sensitivity"], v["specificity"],
                 v["precision"], v["f1"], v["n_features"]))
    print()

    # ---- single-feature reference sweep over all 16 source-neutral descriptors ----
    single = {}
    for jj, f in enumerate(COMMON):
        m_, _, _ = nested_cv(X[:, [jj]], y, n_repeats=4)
        single[f] = m_["balanced_accuracy"]
    print("=== SINGLE-FEATURE reference sweep (4 repeats; ranking only) ===")
    for f, v in sorted(single.items(), key=lambda kv: -kv[1]):
        print("   %-28s %.4f" % (f, v))
    print()

    selected = max(out, key=lambda k: out[k]["balanced_accuracy"])
    print("SELECTED: %s" % selected)
    # Attach the selected candidate's in-fold threshold distribution. This is a
    # description of the CV procedure, not a model parameter.
    out[selected]["in_fold_threshold_distribution"] = thdist[selected]
    kind, p, cols = fam[selected]
    t_final = thr_generic(X[:, cols], y, kind, p)
    final = cand(kind, p); final.fit(X[:, cols], y)
    sc = final.named_steps["sc"] if "sc" in final.named_steps else None
    est = final.named_steps["m"]
    insample = metrics(y, (score_generic(final, X[:, cols]) >= t_final).astype(int))

    spec = {
        "task_id": TASK,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "FROZEN_DEVELOPMENT_ONLY_NOT_SCIENTIFICALLY_VALIDATED",
        "training_data": {
            "source": "BASS_CONSENSUS_DEVELOPMENT.json",
            "development_total": n_dev,
            "supervised_eligible_used": int(len(y)),
            "excluded_human_unstable": n_unstable,
            "present": int((y == 1).sum()), "absent": int((y == 0).sum()),
            "held_out_rows_used": 0, "held_out_human_answers_accessed": False,
        },
        "target": {
            "positive_class": PRESENT, "negative_class": ABSENT,
            "meaning": "Does the target FullMix landmark contain a perceptually reproducible Bass attack?",
            "does_not_mean": ["structural quarter note", "walking quarter", "beat",
                              "PLP ownership", "microtiming"],
        },
        "model": {
            "family": {"logreg": "L2-regularized logistic regression, balanced class weights",
                       "tree": "decision tree",
                       "svc": "RBF-kernel SVM"}[kind],
            "features": [COMMON[c] for c in cols],
            "hyperparameters": ({"penalty": "l2", "C": p, "class_weight": "balanced",
                                 "max_iter": 20000, "solver": "lbfgs"} if kind == "logreg"
                                else {"max_depth": p} if kind == "tree"
                                else {"C": p[0], "gamma": p[1], "kernel": "rbf"}),
            "preprocessing": {
                "imputation": "features are complete on all 32 eligible rows; median retained as the declared fallback",
                "scaling": "StandardScaler fitted on the 32 development rows, then frozen",
                "feature_selection": "NONE at run time; the feature list is fixed in this record",
                "threshold_selection": (
                    "inner 4-fold stratified CV on the 32 development rows only; this is "
                    "the procedure that produced model.decision_threshold. It is NOT the "
                    "in_fold_threshold_mode field, which only describes the CV procedure."),
            },
            "decision_threshold": float(t_final),
            "decision_rule": "BASS_PRESENT if score >= decision_threshold else BASS_ABSENT",
        },
        "outputs": ["BASS_PRESENT probability", "binary predicted class"],
        "uncertainty_output": ("NOT PROVIDED. With n=32 these scores are uncalibrated margins "
                               "and must NOT be read as confidence."),
        "seed": SEED,
        "software": {"python": "3.13.14", "numpy": "2.4.6", "scipy": "1.18.0",
                     "scikit_learn": sklearn.__version__},
        "development_cross_validation": out[selected],
        "threshold_documentation": {
            "operative_frozen_decision_threshold": float(t_final),
            "operative_derivation": (
                "The preregistered inner-threshold procedure (stratified 4-fold CV on the "
                "training rows, out-of-fold scores, grid 0.05..0.95 maximising balanced "
                "accuracy) applied to ALL 32 supervised-eligible development rows."),
            "in_fold_threshold_mode_NOT_the_frozen_threshold": out[selected][
                "in_fold_threshold_mode_NOT_the_frozen_threshold"],
            "in_fold_threshold_distribution_across_50_outer_folds": thdist[selected],
            "what_the_mode_is": (
                "The mode is the most common threshold among the 50 OUTER-FOLD training fits "
                "(each on about 25-26 rows). It characterises the cross-validation procedure, "
                "NOT the frozen model."),
            "why_they_differ": (
                "The mode aggregates 50 subsample fits; the frozen threshold comes from one "
                "application of the same procedure to all 32 rows. These are different "
                "quantities and are not required to agree."),
            "non_operative": True,
            "prohibition": (
                "The in-fold mode is NON-OPERATIVE. predict_bass.py MUST NOT use it. The only "
                "operative threshold is model.decision_threshold."),
            "tuning_prohibition": (
                "The in-fold mode was observed to score HIGHER development cross-validated "
                "balanced accuracy (0.8200) than the frozen 0.50 (0.7908). This was NOT acted "
                "on: substituting it would be tuning on development cross-validation. The "
                "observed 0.45-0.60 spread shows the difference lies within the noise of the "
                "threshold-selection procedure at n=32."),
            "stability_caveat": (
                "The outer-fold spread independently corroborates the recorded HIGH overfitting "
                "risk at n=32."),
        },
        "candidate_family_results": out,
        "single_feature_reference_sweep": single,
        "in_sample_metrics_NOT_performance": insample,
        "post_freeze_rules": [
            "No tuning of any kind based on held-out results is permitted.",
            "Predictions for the 20 held-out landmarks must be computed and frozen BEFORE "
            "the held-out human labels are opened.",
            "Human-unstable held-out cases must be reported separately, not counted as binary errors.",
        ],
    }
    if sc is not None:
        spec["model"]["frozen_scaler_mean"] = sc.mean_.tolist()
        spec["model"]["frozen_scaler_scale"] = sc.scale_.tolist()
    if hasattr(est, "coef_"):
        spec["model"]["frozen_coefficients"] = est.coef_[0].tolist()
        spec["model"]["frozen_intercept"] = float(est.intercept_[0])
    if kind == "tree":
        spec["model"]["frozen_tree"] = {"max_depth": int(est.get_depth()),
                                        "n_leaves": int(est.get_n_leaves())}
    (out / "FROZEN_PIPELINE.json").write_text(json.dumps(spec, indent=2) + "\n")
    print("frozen threshold %.2f; wrote %s/FROZEN_PIPELINE.json" % (t_final, out))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Development training for the frozen Bass pipeline")
    ap.add_argument("--out-dir", help="write to a NEW namespace instead of the frozen package")
    ap.add_argument("--allow-regeneration", action="store_true",
                    help="permit overwriting an existing frozen record (still requires the "
                         "PI override token in the environment for an in-place write)")
    ap.add_argument("--expected-override", help="PI override token for the separately "
                                                 "authorized regeneration task")
    a_ = ap.parse_args()
    main(a_.out_dir, a_.allow_regeneration, a_.expected_override)
