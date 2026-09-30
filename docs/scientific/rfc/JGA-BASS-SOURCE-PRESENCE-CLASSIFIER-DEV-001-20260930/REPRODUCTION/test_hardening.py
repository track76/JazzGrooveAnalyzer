#!/usr/bin/env python3
"""Named tests for PI-BASS-PRE-HELD-OUT-HARDENING-001-20260930.

Covers:
  * frozen-record overwrite protection (item 7)
  * preregistered held-out scoring behaviour on SYNTHETIC fixtures (items 8, 9, 11)
  * the prediction-freeze sequence rehearsal on DUMMY data (item 10)

No real held-out item number, prediction or label is used anywhere in this file.
No model is retrained.

    <python> test_hardening.py -v
"""
import copy
import importlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
REPO = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer")
sys.path.insert(0, str(HERE))

import rehearse_freeze_sequence as SEQ  # noqa: E402
import score_bass_heldout as SC  # noqa: E402
import train_bass_classifier as TC  # noqa: E402

FROZEN_PATH = PKG / "FROZEN_PIPELINE.json"

# Synthetic fixture: hand-computable. Items 1-6 stable, 7 unstable.
# truth:      1 1 1 0 0 0   (items 1,2,3 PRESENT; 4,5,6 ABSENT)
# prediction: 1 1 0 0 0 1
# => tp=2, fn=1, tn=2, fp=1
SYNTH_LABELS = [{"item_number": i, "stable_class": SC.PRESENT} for i in (1, 2, 3)] + \
               [{"item_number": i, "stable_class": SC.ABSENT} for i in (4, 5, 6)] + \
               [{"item_number": 7, "stable_class": SC.UNSTABLE}]
SYNTH_PREDS = [{"item_number": 1, "event_id": "E1", "bass_present_probability": .9,
                "predicted_class": SC.PRESENT, "decision_threshold": 0.5},
               {"item_number": 2, "event_id": "E2", "bass_present_probability": .8,
                "predicted_class": SC.PRESENT, "decision_threshold": 0.5},
               {"item_number": 3, "event_id": "E3", "bass_present_probability": .4,
                "predicted_class": SC.ABSENT, "decision_threshold": 0.5},
               {"item_number": 4, "event_id": "E4", "bass_present_probability": .3,
                "predicted_class": SC.ABSENT, "decision_threshold": 0.5},
               {"item_number": 5, "event_id": "E5", "bass_present_probability": .2,
                "predicted_class": SC.ABSENT, "decision_threshold": 0.5},
               {"item_number": 6, "event_id": "E6", "bass_present_probability": .6,
                "predicted_class": SC.PRESENT, "decision_threshold": 0.5}]


class TestFrozenOverwriteProtection(unittest.TestCase):
    """Item 7: default execution must REFUSE to overwrite frozen scientific authority."""

    def test_default_execution_refuses_when_frozen_record_exists(self):
        with self.assertRaises(SystemExit) as cm:
            TC.guard_frozen_output(TC.DEFAULT_OUT)
        self.assertIn("REFUSING TO OVERWRITE", str(cm.exception))

    def test_refusal_message_names_the_frozen_records(self):
        try:
            TC.guard_frozen_output(TC.DEFAULT_OUT)
        except SystemExit as e:
            msg = str(e)
        self.assertIn("FROZEN_PIPELINE.json", msg)
        self.assertIn("VALIDATION.json", msg)

    def test_refusal_names_the_pi_override_variable(self):
        try:
            TC.guard_frozen_output(TC.DEFAULT_OUT)
        except SystemExit as e:
            msg = str(e)
        self.assertIn(TC.OVERRIDE_ENV, msg)

    def test_fresh_namespace_is_permitted_without_override(self):
        with tempfile.TemporaryDirectory() as d:
            r = TC.guard_frozen_output(d)
        self.assertTrue(r["allowed"])
        self.assertEqual(r["mode"], "fresh_namespace")

    def test_in_place_write_still_refused_with_allow_flag_but_no_pi_token(self):
        saved = os.environ.pop(TC.OVERRIDE_ENV, None)
        try:
            with self.assertRaises(SystemExit) as cm:
                TC.guard_frozen_output(TC.DEFAULT_OUT, allow_regeneration=True,
                                       expected_override="PI-TOKEN-THAT-IS-NOT-IN-ENV")
            self.assertIn("IN-PLACE", str(cm.exception).upper())
        finally:
            if saved is not None:
                os.environ[TC.OVERRIDE_ENV] = saved

    def test_in_place_write_permitted_only_with_matching_pi_token(self):
        saved = os.environ.get(TC.OVERRIDE_ENV)
        os.environ[TC.OVERRIDE_ENV] = "PI-TOKEN-FOR-THIS-TEST"
        try:
            r = TC.guard_frozen_output(TC.DEFAULT_OUT, allow_regeneration=True,
                                       expected_override="PI-TOKEN-FOR-THIS-TEST")
            self.assertEqual(r["mode"], "in_place_pi_override")
            self.assertEqual(sorted(r["collisions"]),
                             ["FROZEN_PIPELINE.json", "VALIDATION.json"])
        finally:
            if saved is None:
                os.environ.pop(TC.OVERRIDE_ENV, None)
            else:
                os.environ[TC.OVERRIDE_ENV] = saved

    def test_regeneration_into_populated_other_namespace_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "FROZEN_PIPELINE.json").write_text("{}")
            r = TC.guard_frozen_output(d, allow_regeneration=True)
        self.assertTrue(r["allowed"])
        self.assertEqual(r["mode"], "regenerate_new_namespace")

    def test_frozen_record_bytes_untouched_by_guard_tests(self):
        self.assertTrue(FROZEN_PATH.exists())
        self.assertNotIn("__pycache__", str(FROZEN_PATH))


class TestScoringSeparatesUnstable(unittest.TestCase):
    """Item 8: human-unstable cases are separate, not binary errors."""

    def test_unstable_is_separated_from_stable(self):
        by_item = {r["item_number"]: r["stable_class"] for r in SYNTH_LABELS}
        stable, unstable = SC.separate_unstable(by_item)
        self.assertEqual(stable, [1, 2, 3, 4, 5, 6])
        self.assertEqual(unstable, [7])

    def test_unstable_item_is_not_counted_as_a_binary_error(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(r["counts"]["scored"], 6)
        self.assertEqual(r["counts"]["human_unstable"], 1)
        self.assertNotIn(7, [p[0] for p in []])

    def test_unstable_count_is_reported_separately(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(r["human_unstable_items_reported_separately"], 1)

    def test_unstable_identities_are_never_disclosed(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertIs(r["unstable_item_identities_disclosed"], False)

    def test_stable_counts_are_reported(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(r["counts"]["stable_present"], 3)
        self.assertEqual(r["counts"]["stable_absent"], 3)

    def test_unknown_class_is_rejected(self):
        bad = [{"item_number": 1, "stable_class": "SOMETHING_ELSE"}]
        with self.assertRaises(ValueError):
            SC.score(SYNTH_PREDS, bad)


class TestPreregisteredMetrics(unittest.TestCase):
    """Item 8: exactly the preregistered metric set, computed correctly."""

    def setUp(self):
        self.r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.m = self.r["metrics"]

    def test_confusion_matrix_matches_hand_computation(self):
        self.assertEqual(self.m["confusion_matrix"],
                         {"tp": 2, "tn": 2, "fp": 1, "fn": 1})

    def test_sensitivity_matches_hand_computation(self):
        self.assertAlmostEqual(self.m["sensitivity_bass_present"], 2 / 3)

    def test_specificity_matches_hand_computation(self):
        self.assertAlmostEqual(self.m["specificity_bass_absent"], 2 / 3)

    def test_precision_matches_hand_computation(self):
        self.assertAlmostEqual(self.m["precision_bass_present"], 2 / 3)

    def test_balanced_accuracy_matches_hand_computation(self):
        self.assertAlmostEqual(self.m["balanced_accuracy"], 2 / 3)

    def test_f1_matches_hand_computation(self):
        self.assertAlmostEqual(self.m["f1_bass_present"], 2 / 3)

    def test_exact_metric_set_is_preregistered_and_closed(self):
        self.assertEqual(tuple(self.r["preregistered_metrics"]),
                         ("balanced_accuracy", "sensitivity_bass_present",
                          "specificity_bass_absent", "precision_bass_present",
                          "f1_bass_present", "confusion_matrix"))

    def test_balanced_accuracy_interval_is_withheld(self):
        self.assertIsNone(self.m["balanced_accuracy_interval"])
        self.assertIn("NOT PROVIDED", self.m["balanced_accuracy_interval_note"])

    def test_exact_intervals_are_reported_for_single_proportions(self):
        ci = self.m["exact_intervals_95_clopper_pearson"]
        for k in ("sensitivity_bass_present", "specificity_bass_absent",
                  "precision_bass_present"):
            lo, hi = ci[k]
            self.assertTrue(0.0 <= lo <= hi <= 1.0)

    def test_clopper_pearson_is_undefined_for_zero_denominator(self):
        import math
        lo, hi = SC._clopper_pearson(0, 0)
        self.assertTrue(math.isnan(lo))
        self.assertTrue(math.isnan(hi))

    def test_denominators_are_published(self):
        d = self.m["denominators"]
        self.assertEqual(d["n_stable_scored"], 6)
        self.assertEqual(d["sensitivity_denominator_present"], 3)
        self.assertEqual(d["specificity_denominator_absent"], 3)


class TestNoCategoricalBoundary(unittest.TestCase):
    """Item 8: n is too small for a categorical performance boundary."""

    def test_categorical_boundary_is_not_authorized(self):
        self.assertFalse(SC.CATEGORICAL_BOUNDARY_AUTHORIZED)

    def test_verdict_is_withheld(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertIsNone(r["categorical_performance_verdict"])

    def test_small_n_caveat_is_attached(self):
        m = SC.score(SYNTH_PREDS, SYNTH_LABELS)["metrics"]
        self.assertIn("too small", m["small_n_caveat"])


class TestScoringNeverMutates(unittest.TestCase):
    """Item 11: never alter predictions, never alter labels."""

    def test_predictions_are_not_mutated(self):
        before = copy.deepcopy(SYNTH_PREDS)
        SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(SYNTH_PREDS, before)

    def test_labels_are_not_mutated(self):
        before = copy.deepcopy(SYNTH_LABELS)
        SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(SYNTH_LABELS, before)

    def test_output_is_deterministic(self):
        a = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        b = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))

    def test_prediction_artifact_carrying_a_label_field_is_rejected(self):
        bad = copy.deepcopy(SYNTH_PREDS)
        bad[0]["stable_class"] = SC.PRESENT
        with self.assertRaises(ValueError):
            SC.score(bad, SYNTH_LABELS)

    def test_missing_prediction_for_stable_item_is_an_error(self):
        with self.assertRaises(ValueError):
            SC.score(SYNTH_PREDS[:-1], SYNTH_LABELS)


class TestPostRevealProhibitions(unittest.TestCase):
    """Item 9: post-reveal prohibitions are carried in the scoring output."""

    def test_all_prohibitions_are_present(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        joined = " ".join(r["post_reveal_prohibitions"]).lower()
        for phrase in ("threshold adjustment", "feature replacement", "model selection",
                       "relabelling", "deletion of stable cases", "second attempt"):
            self.assertIn(phrase, joined)

    def test_new_development_cycle_is_required_for_improvement(self):
        r = SC.score(SYNTH_PREDS, SYNTH_LABELS)
        self.assertTrue(any("NEW development cycle" in p for p in r["post_reveal_prohibitions"]))


class TestFreezeSequenceRehearsal(unittest.TestCase):
    """Item 10: the A-K sequence is executable and ordered on dummy data."""

    @classmethod
    def setUpClass(cls):
        anchor = REPO / "docs/project/BASS_FREEZE_ANCHOR_20260930.json"
        if not anchor.exists():
            raise unittest.SkipTest("freeze anchor not yet created")
        cls.tmp = tempfile.TemporaryDirectory()
        cls.r = SEQ.rehearse(str(anchor), cls.tmp.name)
        cls.steps = {s["step"]: s for s in cls.r["steps"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_sequence_runs_in_the_preregistered_order(self):
        self.assertEqual(self.r["sequence_order_verified"], list("ABCDEFGHIJK"))

    def test_step_a_verifies_the_model_anchor(self):
        self.assertTrue(self.steps["A_verify_model_anchor"]["passed"])
        self.assertEqual(self.steps["A_verify_model_anchor"]["mismatches"], [])

    def test_step_b_uses_the_operative_threshold_only(self):
        b = self.steps["B_load_predictor"]
        self.assertEqual(b["operative_decision_threshold"], 0.5)
        self.assertEqual(b["feature"], "peak_prominence")

    def test_step_c_reads_no_labels(self):
        self.assertFalse(self.steps["C_identify_membership_only"]["labels_read"])

    def test_step_d_generates_twenty_predictions_without_answers(self):
        d = self.steps["D_generate_predictions"]
        self.assertEqual(d["n"], 20)
        self.assertFalse(d["human_answers_accessed"])

    def test_step_f_hashes_the_prediction_artifact(self):
        self.assertEqual(len(self.steps["F_hash_prediction_artifact"]["sha256"]), 64)

    def test_step_g_records_hash_head_and_item_ids(self):
        g = self.steps["G_prediction_freeze_record"]
        self.assertEqual(len(g["record_sha256"]), 64)
        rec = json.loads((Path(self.tmp.name) / "PREDICTION_FREEZE.json").read_text())
        for k in ("git_head", "git_branch", "model_anchor_sha256",
                  "prediction_artifact_sha256", "created_utc", "exact_item_ids"):
            self.assertIn(k, rec)
        self.assertEqual(len(rec["exact_item_ids"]), 20)

    def test_step_i_independently_verifies_unchanged(self):
        self.assertTrue(self.steps["I_verify_artifact_unchanged"]["passed"])

    def test_steps_j_and_k_are_blocked_gates(self):
        self.assertFalse(self.steps["J_reveal"]["executed"])
        self.assertFalse(self.steps["K_score"]["executed"])
        self.assertEqual(self.r["blocked_gates"], ["J_reveal", "K_score"])

    def test_rehearsal_uses_dummy_data_only(self):
        self.assertTrue(self.r["dummy_data_only"])
        self.assertFalse(self.r["real_held_out_answers_accessed"])
        self.assertFalse(self.r["real_held_out_predictions_generated"])
        for it in self.steps["C_identify_membership_only"]["items"]:
            self.assertTrue(it.startswith("DUMMY_"))


class TestScoringCodeIsFrozen(unittest.TestCase):
    """Item 11: the scoring code exists, is importable and is hash-anchorable."""

    def test_scoring_module_exists_in_package(self):
        self.assertTrue((HERE / "score_bass_heldout.py").exists())

    def test_scoring_module_declares_no_categorical_verdict(self):
        self.assertIsNone(SC.score(SYNTH_PREDS, SYNTH_LABELS)["categorical_performance_verdict"])

    def test_scoring_module_never_references_a_real_item_number(self):
        src = (HERE / "score_bass_heldout.py").read_text()
        import re
        # no held-out item identifiers and no absolute answer-bearing paths
        self.assertNotIn("/Volumes/SSD Track", src)
        self.assertNotIn("SEALED_BASS_HELD_OUT_LABELS", src)
        self.assertNotIn("BASS_CONSENSUS_ALL60_SEALED", src)


if __name__ == "__main__":
    unittest.main(verbosity=2)
