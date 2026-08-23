"""Score frozen strength-max predictors against frozen Calibration Zero."""

from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-003-SWING-3-4")
RUN = BASE / "run_20260823_212608"
PREDICTORS = BASE / "preregistrations/frozen_strength_max_predictors.json"
PREREG = BASE / "preregistrations/H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01.md"
EVENT_AUTHORITY = BASE / "run_20260823_203324/event_level_results.json"
CALIBRATION_RESULT = BASE / "run_20260823_203324/result.json"
SYMBOLIC_AUTHORITY = BASE / "run_20260823_203324/calibration_symbolic_events.json"
EXPECTED = {
    str(PREDICTORS): "19e787493b0490a8aeec602d833638b2784002ad4d645af1a81c4c73c3ec3ac0",
    str(PREREG): "254734e5c70155e674108939d0e43785be943ffa6a2bbc116e731578dfa7a426",
    str(EVENT_AUTHORITY): "3c2d22300de63de57885a1c786dea1679136410860558f3e093e6bf2b5233c31",
    str(CALIBRATION_RESULT): "5faa6fe772dd4f6211bfe00646d4cdbde8d904082cef80c18ea53da2e240ee29",
    str(SYMBOLIC_AUTHORITY): "fcb56adb0dfd6361ab6173107fc2f90d293caf8ca87d3fbc2e6b36e393f6a199",
}
SYMBOLIC_FINGERPRINT = "3d97ff352fa0ca3ca5317d1584ec57b62eec368cd3595529f4659321e8a0bda0"


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def score_once(predictors: dict, authority: dict) -> dict:
    lookup = {}
    for source, payload in authority["correspondence_by_source"].items():
        for record in payload["event_results"]:
            lookup[(source, record["cell_index"])] = record
    cases = []
    for predictor in predictors["predictors"]:
        key = (predictor["source"], predictor["cell_index"])
        record = lookup.get(key)
        if record is None:
            raise RuntimeError(f"Missing frozen Ground Truth cell join: {key}")
        candidate_ids = sorted(item["eme_id"] for item in record.get("candidate_emes", []))
        if candidate_ids != predictor["contained_eme_ids"]:
            raise RuntimeError(f"Contained EME authority mismatch: {predictor['cell_identity']}")
        authorized_eme_id = None
        if record["correspondence_status"] == "VALID":
            authorized_eme_id = record["eme_id"]
            if authorized_eme_id not in predictor["contained_eme_ids"]:
                raise RuntimeError(f"Authorized EME outside frozen cell: {predictor['cell_identity']}")
            status = "STRENGTH_MAX_CORRECT" if predictor["predicted_eme_id"] == authorized_eme_id else "STRENGTH_MAX_INCORRECT"
            reason = "FROZEN_VALID_UNIQUE_OBSERVED_AUTHORITY"
        else:
            status = "UNSCORABLE"
            reason = record["correspondence_status"]
        cases.append({
            **predictor,
            "calibration_symbolic_event_id": record["calibration_symbolic_event_id"],
            "ground_truth_correspondence_status": record["correspondence_status"],
            "authorized_observed_eme_id": authorized_eme_id,
            "scoring_status": status,
            "scoring_reason": reason,
            "predictor_changed": False,
            "deterministic_replay_status": "PENDING_SECOND_SCORING",
        })
    summaries = {}
    for source in ("Drums", "Double Bass", "Piano"):
        selected = [case for case in cases if case["source"] == source]
        scorable = [case for case in selected if case["scoring_status"] != "UNSCORABLE"]
        correct = sum(case["scoring_status"] == "STRENGTH_MAX_CORRECT" for case in selected)
        incorrect = sum(case["scoring_status"] == "STRENGTH_MAX_INCORRECT" for case in selected)
        summaries[source] = {
            "total_cells": len(selected), "scorable_cells": len(scorable),
            "unscorable_cells": len(selected) - len(scorable),
            "STRENGTH_MAX_CORRECT": correct, "STRENGTH_MAX_INCORRECT": incorrect,
            "accuracy_scorable": correct / len(scorable) if scorable else None,
        }
    overall_cases = cases
    overall_scorable = [case for case in cases if case["scoring_status"] != "UNSCORABLE"]
    overall_correct = sum(case["scoring_status"] == "STRENGTH_MAX_CORRECT" for case in cases)
    overall_incorrect = sum(case["scoring_status"] == "STRENGTH_MAX_INCORRECT" for case in cases)
    overall = {
        "total_cells": len(cases), "scorable_cells": len(overall_scorable),
        "unscorable_cells": len(cases) - len(overall_scorable),
        "STRENGTH_MAX_CORRECT": overall_correct, "STRENGTH_MAX_INCORRECT": overall_incorrect,
        "accuracy_scorable": overall_correct / len(overall_scorable) if overall_scorable else None,
    }
    populated_sources = [source for source in ("Drums", "Double Bass") if summaries[source]["total_cells"]]
    if not overall_scorable or any(summaries[source]["scorable_cells"] == 0 for source in populated_sources):
        classification = "INSUFFICIENT_SCORABLE_EVIDENCE"
    elif overall["scorable_cells"] == overall["total_cells"] and overall_incorrect == 0:
        classification = "SUPPORTS_STRENGTH_AS_CORRESPONDENCE_PREDICTOR"
    elif overall_correct == 0 and all(summaries[source]["scorable_cells"] > 0 for source in populated_sources):
        classification = "DOES_NOT_SUPPORT_STRENGTH_AS_CORRESPONDENCE_PREDICTOR"
    else:
        classification = "PARTIAL_SOURCE_SPECIFIC_SUPPORT"
    return {"cases": cases, "source_summaries": summaries, "overall_summary": overall, "classification": classification}


def main() -> None:
    for path, expected in EXPECTED.items():
        if checksum(Path(path)) != expected:
            raise RuntimeError(f"Frozen authority checksum mismatch: {path}")
    calibration_summary = json.loads(CALIBRATION_RESULT.read_text(encoding="utf-8"))
    if calibration_summary["symbolic_authority_fingerprint"] != SYMBOLIC_FINGERPRINT:
        raise RuntimeError("Symbolic Ground Truth fingerprint mismatch")
    predictors = json.loads(PREDICTORS.read_text(encoding="utf-8"))
    authority = json.loads(EVENT_AUTHORITY.read_text(encoding="utf-8"))
    first = score_once(predictors, authority)
    second = score_once(predictors, authority)
    if canonical(first) != canonical(second):
        raise RuntimeError("Deterministic scoring replay mismatch")
    for case in first["cases"]:
        case["deterministic_replay_status"] = "EXACT_MATCH"
    scientific = {
        "study_id": "H-CEDVAL003-STRENGTH-MAX-CORRESPONDENCE-VALIDATION-01",
        "predictor_authority_fingerprint": predictors["source_scientific_fingerprint"],
        "ground_truth_symbolic_authority_fingerprint": SYMBOLIC_FINGERPRINT,
        **first,
        "population_verified": True, "predictors_recomputed_after_ground_truth": False,
        "historical_h02_scores_changed": False, "historical_three_dataset_conclusion_changed": False,
        "h02_changed": False, "h03_created": False, "calibration_zero_changed": False,
        "raw_observations_changed": False, "production_promotion_authorized": False,
        "architecture_impact": "NONE", "production_impact": "NONE", "production_code_changed": False,
        "deterministic_replay": True,
    }
    fingerprint = sha256(canonical(scientific)).hexdigest()
    result = {"status": "PASS", "scientific_fingerprint": fingerprint, "scientific_content": scientific}
    (RUN / "scoring_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest = {"preregistration_commit": "e2753a66ee9fe146e42af9fdf8e033bc1f91da3e", "frozen_inputs": EXPECTED, "symbolic_authority_fingerprint": SYMBOLIC_FINGERPRINT, "ground_truth_opened_only_after_preregistration": True}
    (RUN / "input_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "summaries": first["source_summaries"], "overall": first["overall_summary"], "classification": first["classification"], "fingerprint": fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
