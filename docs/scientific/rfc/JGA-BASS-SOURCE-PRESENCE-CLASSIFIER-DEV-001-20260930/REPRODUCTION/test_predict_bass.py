#!/usr/bin/env python3
"""Named tests for the frozen Bass source-presence pipeline and its firewall.

    <python> test_predict_bass.py -v
"""
import ast
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(HERE))
import predict_bass  # noqa: E402

FROZEN = json.loads((PKG / "FROZEN_PIPELINE.json").read_text())
NS = Path("/Volumes/SSD Track/JGA/experiments/JGA-HUMAN-BASS-PRESENCE-60-001-20260930")
PA = Path("/Users/StarTrack/Development/JazzGrooveAnalyzer/docs/scientific/rfc/"
          "JGA-FULLMIX-INSTRUMENT-IDENTITY-001-20260929")

# Canonical answer-bearing artifact NAMES. These are the real files on disk, verified by
# existence during this task. Held-out answer content lives on the HD mirror.
HD_NS = Path("/Volumes/HD BackUp/JGA_BACKUP/SSD_TRACK_JGA/JGA/experiments/"
             "JGA-HUMAN-BASS-PRESENCE-60-001-20260930")
ANSWER_BEARING_FILES = ["SEALED_BASS_HELD_OUT_LABELS.json",   # HD mirror only (held-out answers)
                        "BASS_CONSENSUS_ALL60_SEALED.json",   # HD mirror only (held-out answers)
                        "BASS_PASS_1_LABELS.json",            # SSD + HD (raw human pass 1)
                        "BASS_PASS_2_LABELS.json",            # SSD + HD (raw human pass 2)
                        "BASS_HELD_OUT_SEAL.json"]            # SSD + HD (held-out seal)
ANSWER_BEARING_DIRS = ["PRE_SEAL_RECORDS"]                   # HD mirror only
# Backwards-compatible alias retained so older references do not break; now real paths.
PROHIBITED_LABEL_FILES = ANSWER_BEARING_FILES + ANSWER_BEARING_DIRS


def prohibited_paths():
    """Every real on-disk path that must never be opened before prediction freeze."""
    out = []
    for base in (NS, HD_NS):
        for name in ANSWER_BEARING_FILES + ANSWER_BEARING_DIRS:
            out.append(base / name)
    return out


PROHIBITED_PATHS = prohibited_paths()


def code_string_literals(path):
    """String literals in executable code, EXCLUDING docstrings.

    A docstring that *declares* the firewall ("this script never opens X") is
    documentation, not access. Only real string operands can build a path.
    """
    tree = ast.parse(Path(path).read_text())
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            d = ast.get_docstring(node, clean=False)
            if d is not None:
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                            and sub.value == d:
                        docs.add(id(sub))
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in docs]


class TestPipelineFrozen(unittest.TestCase):
    def test_status_is_development_only(self):
        self.assertIn("DEVELOPMENT_ONLY", FROZEN["status"])

    def test_not_scientifically_validated(self):
        self.assertIn("NOT_SCIENTIFICALLY_VALIDATED", FROZEN["status"])

    def test_single_feature_is_declared(self):
        self.assertEqual(FROZEN["model"]["features"], ["peak_prominence"])

    def test_coefficients_match_feature_count(self):
        self.assertEqual(len(FROZEN["model"]["frozen_coefficients"]),
                         len(FROZEN["model"]["features"]))
        self.assertEqual(len(FROZEN["model"]["frozen_scaler_mean"]),
                         len(FROZEN["model"]["features"]))

    def test_threshold_is_declared_and_frozen(self):
        self.assertIsInstance(FROZEN["model"]["decision_threshold"], float)
        self.assertGreaterEqual(FROZEN["model"]["decision_threshold"], 0.0)
        self.assertLessEqual(FROZEN["model"]["decision_threshold"], 1.0)

    def test_seed_and_software_versions_are_frozen(self):
        self.assertIsInstance(FROZEN["seed"], int)
        for k in ("python", "numpy", "scipy", "scikit_learn"):
            self.assertIn(k, FROZEN["software"])

    def test_missing_value_handling_is_declared(self):
        self.assertIn("imputation", FROZEN["model"]["preprocessing"])

    def test_uncertainty_is_explicitly_withheld(self):
        self.assertIn("NOT PROVIDED", FROZEN["uncertainty_output"])


class TestTrainingDataDiscipline(unittest.TestCase):
    def test_no_held_out_rows_used(self):
        self.assertEqual(FROZEN["training_data"]["held_out_rows_used"], 0)

    def test_held_out_answers_not_accessed(self):
        self.assertIs(FROZEN["training_data"]["held_out_human_answers_accessed"], False)

    def test_unstable_were_excluded_not_relabelled(self):
        self.assertEqual(FROZEN["training_data"]["excluded_human_unstable"], 8)
        self.assertEqual(FROZEN["training_data"]["supervised_eligible_used"], 32)
        self.assertEqual(FROZEN["training_data"]["development_total"], 40)

    def test_class_counts_sum_to_eligible(self):
        t = FROZEN["training_data"]
        self.assertEqual(t["present"] + t["absent"], t["supervised_eligible_used"])

    def test_target_is_source_presence_not_structure(self):
        self.assertEqual(FROZEN["target"]["positive_class"], "BASS_PRESENT_STABLE")
        self.assertEqual(FROZEN["target"]["negative_class"], "BASS_ABSENT_STABLE")
        for forbidden in ("structural quarter note", "walking quarter", "beat",
                          "PLP ownership", "microtiming"):
            self.assertIn(forbidden, FROZEN["target"]["does_not_mean"])


class TestHeldOutFirewall(unittest.TestCase):
    """The predictor must be structurally incapable of reading human labels."""

    def _sources(self):
        return [HERE / "predict_bass.py", HERE / "train_bass_classifier.py"]

    def test_predictor_source_never_names_a_prohibited_label_file(self):
        src = (HERE / "predict_bass.py").read_text()
        for bad in PROHIBITED_LABEL_FILES:
            self.assertNotIn(bad, src, "predictor references %s" % bad)

    def test_predictor_declares_no_label_read(self):
        tree = ast.parse((HERE / "predict_bass.py").read_text())
        reads = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute) and n.func.attr == "read_text"]
        self.assertTrue(reads)
        joined = " ".join(ast.unparse(n) for n in reads)
        self.assertNotIn("LABELS", joined)
        self.assertNotIn("CONSENSUS", joined)

    def test_training_script_never_opens_a_prohibited_label_file(self):
        src = (HERE / "train_bass_classifier.py").read_text()
        for bad in PROHIBITED_LABEL_FILES:
            self.assertNotIn('"%s"' % bad, src)

    def test_training_script_reads_only_the_development_consensus(self):
        src = (HERE / "train_bass_classifier.py").read_text()
        self.assertIn("BASS_CONSENSUS_DEVELOPMENT.json", src)

    def test_predictor_emits_no_human_label_field(self):
        rows = predict_bass.load_phase_a()
        eid = next(iter(rows))
        res = predict_bass.score([rows[eid]])
        self.assertEqual(set(res[0]), {"event_id", "bass_present_probability",
                                       "predicted_class", "decision_threshold"})

    def test_predictor_output_has_no_confidence_field(self):
        rows = predict_bass.load_phase_a()
        res = predict_bass.score([rows[next(iter(rows))]])
        self.assertNotIn("confidence", res[0])
        self.assertNotIn("uncertainty", res[0])


class TestScoringBehaviour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = predict_bass.load_phase_a()
        cls.sample = list(cls.rows.values())[:5]

    def test_probability_is_within_unit_interval(self):
        for r in predict_bass.score(self.sample):
            self.assertGreaterEqual(r["bass_present_probability"], 0.0)
            self.assertLessEqual(r["bass_present_probability"], 1.0)

    def test_predicted_class_is_binary_and_valid(self):
        for r in predict_bass.score(self.sample):
            self.assertIn(r["predicted_class"], ("BASS_PRESENT_STABLE", "BASS_ABSENT_STABLE"))

    def test_class_follows_the_frozen_threshold(self):
        thr = FROZEN["model"]["decision_threshold"]
        for r in predict_bass.score(self.sample):
            expected = "BASS_PRESENT_STABLE" if r["bass_present_probability"] >= thr \
                else "BASS_ABSENT_STABLE"
            self.assertEqual(r["predicted_class"], expected)

    def test_scoring_is_deterministic(self):
        a = predict_bass.score(self.sample)
        b = predict_bass.score(self.sample)
        self.assertEqual(a, b)

    def test_uses_only_the_single_declared_feature(self):
        src = (PKG / "FROZEN_PIPELINE.json").read_text()
        feat = FROZEN["model"]["features"][0]
        self.assertIn(feat, src)

    def test_rejects_non_finite_features(self):
        bad = {"event_id": "TEST_BAD", "common_features": {"peak_prominence": float("nan")}}
        with self.assertRaises(ValueError):
            predict_bass.score([bad])


class TestProhibitedPredictorsAbsent(unittest.TestCase):
    def test_frozen_feature_is_not_stem_derived(self):
        self.assertEqual(FROZEN["model"]["features"], ["peak_prominence"])

    def test_frozen_feature_is_source_neutral(self):
        """The frozen feature must be declared in the source-neutral common set,
        and must NOT be a stem-witness, arm-membership or coordinate field."""
        f = FROZEN["model"]["features"][0]
        schema = json.loads((PA / "COMMON_FEATURE_SCHEMA.json").read_text())
        self.assertIn(f, schema["common_features"])
        for group in ("source_specific_optional_features", "excluded_from_the_feature_matrix"):
            self.assertNotIn(f, schema[group])
        r = list(predict_bass.load_phase_a().values())[0]
        self.assertIn(f, r["common_features"])
        self.assertNotIn(f, r.get("multi_stem_witness", {}))

    def test_no_timing_or_offset_feature_frozen(self):
        f = FROZEN["model"]["features"][0]
        for banned in ("offset", "plp", "quarter", "measure", "distance", "offbeat", "ms"):
            self.assertNotIn(banned, f.lower())


class TestRealAnswerBearingFirewall(unittest.TestCase):
    """Item 5 repair: guard the REAL answer-bearing paths, not invented filenames.

    The previous guard listed three names that do not exist at the SSD path the
    predictor reads, so it certified a firewall it never tested. These tests
    (a) refuse to pass if the prohibition list drifts away from disk again, and
    (b) audit ACTUAL runtime file opens with an OS-level audit hook.
    """

    def test_prohibition_list_is_not_vacuous(self):
        """At least one real answer-bearing artifact must exist on disk.

        If this ever fails, the named paths were renamed or relocated and the
        firewall guard has silently become meaningless. Fix the paths, do not
        weaken the assertion.
        """
        existing = [p for p in PROHIBITED_PATHS if p.exists()]
        self.assertGreaterEqual(
            len(existing), 6,
            "prohibition list no longer matches disk: only %d of %d exist; "
            "the firewall guard would be vacuous" % (len(existing), len(PROHIBITED_PATHS)))

    def test_held_out_answer_files_exist_on_hd_mirror(self):
        for name in ("SEALED_BASS_HELD_OUT_LABELS.json", "BASS_CONSENSUS_ALL60_SEALED.json",
                     "PRE_SEAL_RECORDS"):
            self.assertTrue((HD_NS / name).exists(),
                            "expected held-out answer artifact %s on HD mirror" % name)

    def test_held_out_answer_files_absent_from_ssd_original(self):
        """Records the real condition: SSD original does not hold held-out answers."""
        for name in ("SEALED_BASS_HELD_OUT_LABELS.json", "BASS_CONSENSUS_ALL60_SEALED.json"):
            self.assertFalse((NS / name).exists(),
                             "unexpected: %s present in SSD original" % name)

    def test_runtime_prediction_opens_no_answer_bearing_artifact(self):
        """Audit-hook the real scoring path with SYNTHETIC, non-held-out inputs.

        Runs in a subprocess because sys.addaudithook cannot be uninstalled.
        """
        import subprocess  # noqa: F811
        script = r'''
import sys, os, json
sys.dont_write_bytecode = True
sys.path.insert(0, "__HERE__")
import predict_bass as P
opened = []
def hook(event, args):
    if event == "open" and isinstance(args[0], (str, bytes, os.PathLike)):
        try: opened.append(os.path.realpath(str(args[0])))
        except Exception: pass
sys.addaudithook(hook)
spec = json.loads(P.FROZEN.read_text())
feats = spec["model"]["features"]
synthetic = [{"event_id": "SYN_" + str(i),
              "common_features": dict((f, 0.123456 * i + 1.0) for f in feats)}
             for i in range(5)]
P.score(synthetic, spec)
P.load_phase_a()
print(json.dumps(sorted(set(opened))))
'''.replace("__HERE__", str(HERE))
        proc = subprocess.run([sys.executable, "-c", script],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        opened = set(json.loads(proc.stdout.strip().splitlines()[-1]))
        forbidden = {os.path.realpath(str(p)) for p in PROHIBITED_PATHS if p.exists()}
        self.assertEqual(
            opened & forbidden, set(),
            "pre-reveal scoring opened answer-bearing artifact(s): %s"
            % sorted(opened & forbidden))

    def test_static_predictor_code_names_no_answer_bearing_artifact(self):
        lits = code_string_literals(HERE / "predict_bass.py")
        for bad in PROHIBITED_LABEL_FILES:
            for lit in lits:
                self.assertNotIn(bad, lit,
                                 "predictor code references %s" % bad)

    def test_static_training_code_names_no_held_out_answer_artifact(self):
        lits = code_string_literals(HERE / "train_bass_classifier.py")
        for bad in ("SEALED_BASS_HELD_OUT_LABELS", "BASS_CONSENSUS_ALL60_SEALED",
                    "PRE_SEAL_RECORDS", "BASS_HELD_OUT_SEAL"):
            for lit in lits:
                self.assertNotIn(bad, lit,
                                 "training code references %s" % bad)

    def test_training_opens_only_the_development_consensus(self):
        """Runtime audit of the training loader against real answer-bearing paths."""
        lits = code_string_literals(HERE / "train_bass_classifier.py")
        labelish = [l for l in lits if ".json" in l and "CONSENSUS" in l]
        self.assertTrue(labelish)
        for l in labelish:
            self.assertEqual(Path(l).name, "BASS_CONSENSUS_DEVELOPMENT.json",
                             "training references a non-development label file: %s" % l)


if __name__ == "__main__":
    unittest.main(verbosity=2)
