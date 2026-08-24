"""Execute frozen H-CEDVAL004-PULSECANDIDATE-STRENGTH-PHYSICAL-PREDICTION-01."""
from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
import platform
from pathlib import Path
import sys
import wave

import librosa

from jga.pipeline.default_analysis_pipeline import AnalysisPipeline

BASE = Path("validation/CED-VAL-004-PHYSICAL-ONSET")
RUN = BASE / "run_20260824_115749"
EXTERNAL = Path("/Volumes/SSD Track/JGA")
AUTHORITY = BASE / "input_authority_manifest.json"
SCHEDULE = BASE / "event_schedule.json"
PHYSICAL = BASE / "run_20260824_110800/event_level_physical_onsets.json"
PHYSICAL_TO_JGA = BASE / "run_20260824_112730/scientific_content.json"
PREREG = BASE / "preregistrations/H-CEDVAL004-PULSECANDIDATE-STRENGTH-PHYSICAL-PREDICTION-01.md"
STUDY_ID = "H-CEDVAL004-PULSECANDIDATE-STRENGTH-PHYSICAL-PREDICTION-01"
EXECUTION_ID = "EXEC-CEDVAL004-STRENGTH-PHYSICAL-PREDICTION-20260824-115749"
PREREG_COMMIT = "609d506625ac4fd080122a8052e415bab5f83f88"
DATASET_FP = "704ce5926852a2ff62d9794dbee48156f875016979214cf7ef3ab93aa35ec772"
PHYSICAL_FP = "7b2ec48f0ff0afca54849b5847f5ebd637c8d672eb2b88247ea6a1841af99062"
PHYSICAL_TO_JGA_FP = "cebccb70224dce4e519197e84178e11afdc1e98b8148914a7512ac6df06ef22e"
SR, HOP, SCOPE = 44100, 512, 8820000
EXPECTED = {
    str(PREREG): "f5e86bb34a6bcf5c37dcc0f9b5bc6d4763822fb1de72bad22e8e5dfb69c7a4be",
    str(AUTHORITY): "823893f86f5d8a8b68e5ef57dce47739454897e93321dac1b815c735330d429a",
    str(SCHEDULE): "458227636da615278d5334039630f916d1b8be200587c37ae16a4673e8afe2dc",
    str(PHYSICAL): "e8860a248325f5080077f51c833f39884c63cbedaa1671f549a6a7465729d7b2",
    str(PHYSICAL_TO_JGA): "4db4df89aedb224703bf7f06b44bdd4d839221714c7a367552915f9d7d55e39e",
    "src/jga/pipeline/default_analysis_pipeline.py": "04ecdfee536717b977276b91b7e9416701e7a89ce9aa7bc4339917263725ef17",
    "src/jga/engines/source_pulse_candidate_builder.py": "5b270f352483dde91448b0958a299c08e51d064ab867bc872ef1cdde37a81c32",
    "src/jga/engines/domain_pulse_candidate_adapter.py": "6a3d276bf50534bc6823075a26787c624ab7a8d2ecca58628579fb86658a9330",
    "src/jga/domain/pulse_candidate.py": "d397b12b84eb07d44e3b02f0055ab9e645ded07fb5139a49df74fc4f615099d7",
}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def checksum(path):
    digest = sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def exact(value):
    return f"{value.numerator}/{value.denominator}"

def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

def verify_gate():
    for path, expected in EXPECTED.items():
        if checksum(path) != expected:
            raise RuntimeError(f"AUTHORITY_CONFLICT checksum: {path}")
    authority = json.loads(AUTHORITY.read_text())
    frozen_fp = authority.pop("dataset_fingerprint")
    if frozen_fp != DATASET_FP or sha256(canonical(authority)).hexdigest() != frozen_fp:
        raise RuntimeError("AUTHORITY_CONFLICT dataset fingerprint")
    schedule = json.loads(SCHEDULE.read_text())
    schedule_fp = schedule.pop("schedule_fingerprint")
    if sha256(canonical(schedule)).hexdigest() != schedule_fp:
        raise RuntimeError("AUTHORITY_CONFLICT schedule fingerprint")
    if [e["marker_sample"] for e in schedule["events"]] != [88200 + 441000 * k for k in range(20)]:
        raise RuntimeError("AUTHORITY_CONFLICT schedule")
    comparison = json.loads(PHYSICAL_TO_JGA.read_text())
    if comparison["dataset_fingerprint"] != DATASET_FP or comparison["physical_authority_fingerprint"] != PHYSICAL_FP:
        raise RuntimeError("AUTHORITY_CONFLICT physical-to-JGA binding")
    assets, paths = {}, {}
    for source in ("Drums", "Double Bass"):
        ref = authority["canonical_assets"][source]
        path = EXTERNAL / ref["path"]
        if checksum(path) != ref["sha256"]:
            raise RuntimeError(f"AUTHORITY_CONFLICT source checksum: {source}")
        with wave.open(str(path), "rb") as stream:
            props = (stream.getnchannels(), stream.getsampwidth(), stream.getframerate(), stream.getnframes(), stream.getcomptype())
        if props != (2, 3, SR, SCOPE, "NONE"):
            raise RuntimeError(f"AUTHORITY_CONFLICT source properties: {source}")
        paths[source] = path
        assets[source] = {**ref, "channels": 2, "sample_width_bytes": 3, "sample_rate_hz": SR, "frame_count": SCOPE}
    return schedule, schedule_fp, paths, assets

def observe_without_strength(paths):
    stripped, private = {}, {}
    for source, path in paths.items():
        context = AnalysisPipeline().analyze(str(path))
        source_records, source_private = [], {}
        for candidate in context.domain_pulse_candidates:
            frame = round(candidate.timestamp * SR / HOP)
            rebuilt = float(librosa.frames_to_time(frame, sr=SR, hop_length=HOP))
            if rebuilt.hex() != candidate.timestamp.hex():
                raise RuntimeError(f"CANDIDATE_AUTHORITY_CONFLICT frame: {candidate.id}")
            identity = str(candidate.id)
            record = {
                "pulse_candidate_id": identity,
                "source": source,
                "sound_source_id": str(candidate.sound_source_id),
                "observation_index": candidate.observation_index,
                "observation_provenance_id": candidate.observation_provenance_id,
                "timestamp_binary64": candidate.timestamp,
                "timestamp_hex": candidate.timestamp.hex(),
                "producer_frame": frame,
                "n_candidate": HOP * frame,
            }
            source_records.append(record)
            source_private[identity] = candidate
        if len(source_records) != len({r["pulse_candidate_id"] for r in source_records}):
            raise RuntimeError(f"CANDIDATE_AUTHORITY_CONFLICT duplicate identity: {source}")
        stripped[source] = sorted(source_records, key=lambda r: (r["n_candidate"], r["pulse_candidate_id"]))
        private[source] = source_private
    return stripped, private

def construct_populations(schedule, observed):
    populations = []
    for source in ("Drums", "Double Bass"):
        events = [e for e in schedule["events"] if e["source"] == source]
        markers = [e["marker_sample"] for e in events]
        boundaries = [Fraction(markers[i] + markers[i + 1], 2) for i in range(9)]
        for index, event in enumerate(events):
            left = Fraction(0) if index == 0 else boundaries[index - 1]
            right = Fraction(SCOPE) if index == 9 else boundaries[index]
            boundary_candidates = [c for c in observed[source] if Fraction(c["n_candidate"]) in boundaries and (Fraction(c["n_candidate"]) == left or Fraction(c["n_candidate"]) == right)]
            eligible = [c for c in observed[source] if left <= c["n_candidate"] < right and Fraction(c["n_candidate"]) not in boundaries]
            if boundary_candidates:
                status = "CANDIDATE_AUTHORITY_CONFLICT"
            elif len(eligible) == 0:
                status = "NO_CANDIDATES"
            elif len(eligible) == 1:
                status = "SINGLETON_CANDIDATE_POPULATION"
            else:
                status = "NONVACUOUS_CANDIDATE_POPULATION"
            populations.append({
                "event_id": event["event_id"], "source": source, "marker_sample": event["marker_sample"],
                "cell": {"left_exact": exact(left), "right_exact": exact(right), "left_closed": True, "right_open": True},
                "population_status": status, "candidate_count": len(eligible),
                "candidate_ids": [c["pulse_candidate_id"] for c in eligible], "candidates": eligible,
                "boundary_candidate_ids": [c["pulse_candidate_id"] for c in boundary_candidates],
            })
    return populations

def predict(populations, private):
    predictions, strength_access_count = [], 0
    for population in populations:
        out = {k: v for k, v in population.items() if k != "candidates"}
        out.update({"predictor_status": None, "predicted_pulse_candidate_id": None, "strengths": []})
        if population["population_status"] == "NONVACUOUS_CANDIDATE_POPULATION":
            strengths = []
            for record in population["candidates"]:
                value = private[population["source"]][record["pulse_candidate_id"]].strength
                strength_access_count += 1
                strengths.append({"pulse_candidate_id": record["pulse_candidate_id"], "strength_binary64": value, "strength_hex": value.hex()})
            maximum = max(x["strength_binary64"] for x in strengths)
            winners = [x for x in strengths if x["strength_binary64"] == maximum]
            out["strengths"] = sorted(strengths, key=lambda x: x["pulse_candidate_id"])
            if len(winners) == 1:
                out["predictor_status"] = "PREDICTED_PULSECANDIDATE"
                out["predicted_pulse_candidate_id"] = winners[0]["pulse_candidate_id"]
            else:
                out["predictor_status"] = "STRENGTH_TIED"
        predictions.append(out)
    return predictions, strength_access_count

def score(predictions, populations):
    # This is the first read of event-level physical coordinates.
    physical_doc = json.loads(PHYSICAL.read_text())
    if physical_doc["scientific_fingerprint"] != PHYSICAL_FP:
        raise RuntimeError("AUTHORITY_CONFLICT physical fingerprint")
    physical = {r["event_id"]: r for r in physical_doc["records"]}
    population_by_event = {p["event_id"]: p for p in populations}
    scored = []
    for prediction in predictions:
        out = dict(prediction)
        out.update({"physical_authority_opened_after_blind_freeze": True, "n_physical": None, "distances": [], "physical_nearest_pulse_candidate_id": None, "scoring_status": None})
        if prediction["population_status"] == "NONVACUOUS_CANDIDATE_POPULATION" and prediction["predictor_status"] == "PREDICTED_PULSECANDIDATE":
            n_physical = physical[prediction["event_id"]]["n_physical"]
            candidates = population_by_event[prediction["event_id"]]["candidates"]
            distances = [{"pulse_candidate_id": c["pulse_candidate_id"], "n_candidate": c["n_candidate"], "absolute_distance_samples": abs(c["n_candidate"] - n_physical)} for c in candidates]
            minimum = min(d["absolute_distance_samples"] for d in distances)
            winners = [d for d in distances if d["absolute_distance_samples"] == minimum]
            out["n_physical"] = n_physical
            out["distances"] = sorted(distances, key=lambda d: d["pulse_candidate_id"])
            if len(winners) > 1:
                out["scoring_status"] = "PHYSICAL_OUTCOME_TIED"
            else:
                nearest = winners[0]["pulse_candidate_id"]
                out["physical_nearest_pulse_candidate_id"] = nearest
                out["scoring_status"] = "STRENGTH_MAX_CORRECT" if nearest == prediction["predicted_pulse_candidate_id"] else "STRENGTH_MAX_INCORRECT"
        scored.append(out)
    return scored

def summarize(scored):
    result = {}
    for source in ("Drums", "Double Bass"):
        rows = [r for r in scored if r["source"] == source]
        correct = sum(r["scoring_status"] == "STRENGTH_MAX_CORRECT" for r in rows)
        incorrect = sum(r["scoring_status"] == "STRENGTH_MAX_INCORRECT" for r in rows)
        denominator = correct + incorrect
        result[source] = {
            "total_event_cells": len(rows),
            "no_candidate_count": sum(r["population_status"] == "NO_CANDIDATES" for r in rows),
            "singleton_count": sum(r["population_status"] == "SINGLETON_CANDIDATE_POPULATION" for r in rows),
            "non_vacuous_count": sum(r["population_status"] == "NONVACUOUS_CANDIDATE_POPULATION" for r in rows),
            "candidate_authority_conflict_count": sum(r["population_status"] == "CANDIDATE_AUTHORITY_CONFLICT" for r in rows),
            "strength_tied_count": sum(r["predictor_status"] == "STRENGTH_TIED" for r in rows),
            "strength_unresolved_count": sum(r["predictor_status"] == "STRENGTH_UNRESOLVED" for r in rows),
            "physical_outcome_tied_count": sum(r["scoring_status"] == "PHYSICAL_OUTCOME_TIED" for r in rows),
            "scorable_count": denominator, "correct_count": correct, "incorrect_count": incorrect,
            "accuracy_exact": None if denominator == 0 else exact(Fraction(correct, denominator)),
        }
    return result

def classify(summary):
    if any(summary[s]["non_vacuous_count"] == 0 for s in ("Drums", "Double Bass")):
        return "INSUFFICIENT_NONVACUOUS_CANDIDATES"
    if any(summary[s]["scorable_count"] == 0 for s in ("Drums", "Double Bass")):
        return "INSUFFICIENT_SCORABLE_EVIDENCE"
    total_non = sum(summary[s]["non_vacuous_count"] for s in summary)
    total_scorable = sum(summary[s]["scorable_count"] for s in summary)
    total_correct = sum(summary[s]["correct_count"] for s in summary)
    if total_scorable == total_non and total_correct == total_scorable:
        return "SUPPORTS_STRENGTH_AS_PHYSICAL_CANDIDATE_PREDICTOR"
    if total_correct == 0:
        return "DOES_NOT_SUPPORT_STRENGTH_AS_PHYSICAL_CANDIDATE_PREDICTOR"
    return "PARTIAL_SOURCE_SPECIFIC_SUPPORT"

def main():
    schedule, schedule_fp, paths, assets = verify_gate()
    observed1, private1 = observe_without_strength(paths)
    populations1 = construct_populations(schedule, observed1)
    population_basis1 = {"study_id": STUDY_ID, "dataset_fingerprint": DATASET_FP, "schedule_fingerprint": schedule_fp, "observed": observed1, "populations": populations1, "t_physical_accessed": False, "strength_accessed": False}
    population_fp1 = sha256(canonical(population_basis1)).hexdigest()
    predictions1, strength_count1 = predict(populations1, private1)
    predictor_basis1 = {"population_fingerprint": population_fp1, "predictions": predictions1}
    predictor_fp1 = sha256(canonical(predictor_basis1)).hexdigest()

    observed2, private2 = observe_without_strength(paths)
    populations2 = construct_populations(schedule, observed2)
    population_basis2 = {"study_id": STUDY_ID, "dataset_fingerprint": DATASET_FP, "schedule_fingerprint": schedule_fp, "observed": observed2, "populations": populations2, "t_physical_accessed": False, "strength_accessed": False}
    population_fp2 = sha256(canonical(population_basis2)).hexdigest()
    predictions2, strength_count2 = predict(populations2, private2)
    predictor_fp2 = sha256(canonical({"population_fingerprint": population_fp2, "predictions": predictions2})).hexdigest()
    if canonical((observed1, populations1, predictions1, population_fp1, predictor_fp1, strength_count1)) != canonical((observed2, populations2, predictions2, population_fp2, predictor_fp2, strength_count2)):
        raise RuntimeError("DETERMINISTIC_BLIND_REPLAY_CONFLICT")

    scored1 = score(predictions1, populations1)
    scored2 = score(predictions2, populations2)
    summary1, summary2 = summarize(scored1), summarize(scored2)
    if canonical((scored1, summary1)) != canonical((scored2, summary2)):
        raise RuntimeError("DETERMINISTIC_SCORING_REPLAY_CONFLICT")
    classification = classify(summary1)
    overall_correct = sum(summary1[s]["correct_count"] for s in summary1)
    overall_incorrect = sum(summary1[s]["incorrect_count"] for s in summary1)
    overall_scorable = overall_correct + overall_incorrect
    overall = {"non_vacuous_count": sum(summary1[s]["non_vacuous_count"] for s in summary1), "scorable_count": overall_scorable, "correct_count": overall_correct, "incorrect_count": overall_incorrect, "accuracy_exact": None if overall_scorable == 0 else exact(Fraction(overall_correct, overall_scorable))}
    scientific = {
        "study_id": STUDY_ID, "dataset_fingerprint": DATASET_FP, "physical_authority_fingerprint": PHYSICAL_FP,
        "physical_to_jga_fingerprint": PHYSICAL_TO_JGA_FP, "population_fingerprint": population_fp1,
        "blind_predictor_fingerprint": predictor_fp1, "populations": populations1, "blind_predictions": predictions1,
        "event_level_scoring": scored1, "source_summary": summary1, "overall_summary": overall,
        "classification": classification, "deterministic_replay": "PASS_EXACT",
        "strength_values_accessed_count": strength_count1, "t_physical_opened_only_after_blind_freeze": True,
        "frame_authority": {"hop_samples": HOP, "sample_rate_hz": SR, "spacing_seconds_exact": "512/44100", "sample_level_candidate_precision_claimed": False},
        "firewalls": {"jga_tuned": False, "historical_results_changed": False, "h02_changed": False, "h03_created": False, "physical_authority_changed": False, "production_code_changed": False},
    }
    scientific_fp = sha256(canonical(scientific)).hexdigest()
    input_manifest = {"authority_gate": "PASS", "study_id": STUDY_ID, "preregistration_commit": PREREG_COMMIT, "dataset_fingerprint": DATASET_FP, "physical_authority_fingerprint": PHYSICAL_FP, "physical_to_jga_fingerprint": PHYSICAL_TO_JGA_FP, "checksums": EXPECTED, "assets": assets, "environment": {"python": sys.version, "platform": platform.platform(), "librosa": librosa.__version__}}
    result = {"status": "PASS_FROZEN_PROSPECTIVE_RESULT", "classification": classification, "blind_population_fingerprint": population_fp1, "blind_predictor_fingerprint": predictor_fp1, "scientific_fingerprint": scientific_fp, "source_summary": summary1, "overall_summary": overall, "deterministic_replay": "PASS_EXACT", "strength_values_accessed_count": strength_count1, "t_physical_opened_only_after_blind_freeze": True, "firewalls": scientific["firewalls"]}
    write_json(RUN / "input_manifest.json", input_manifest)
    write_json(RUN / "observed_populations_without_strength.json", observed1)
    write_json(RUN / "blind_candidate_populations.json", {"blind_population_fingerprint": population_fp1, "populations": populations1})
    write_json(RUN / "blind_strength_predictions.json", {"blind_predictor_fingerprint": predictor_fp1, "predictions": predictions1, "strength_values_accessed_count": strength_count1})
    write_json(RUN / "event_level_scoring.json", scored1)
    write_json(RUN / "source_summary.json", summary1)
    write_json(RUN / "scientific_content.json", scientific)
    write_json(RUN / "result.json", result)
    write_json(RUN / "completion_protocol.json", {"study_id": STUDY_ID, "authority_gate": "PASS", "blind_replay": "PASS_EXACT", "scoring_replay": "PASS_EXACT", "classification": classification, "scientific_fingerprint": scientific_fp})
    lines = [f"# {STUDY_ID} frozen execution result", "", f"Status: **{classification}**", "", f"Scientific fingerprint: `{scientific_fp}`.", "", f"Blind population fingerprint: `{population_fp1}`.", "", f"Blind predictor fingerprint: `{predictor_fp1}`.", ""]
    for source in ("Drums", "Double Bass"):
        s = summary1[source]
        lines += [f"## {source}", "", f"Cells {s['total_event_cells']}; empty {s['no_candidate_count']}; singleton {s['singleton_count']}; non-vacuous {s['non_vacuous_count']}; conflicts {s['candidate_authority_conflict_count']}; scorable {s['scorable_count']}; correct {s['correct_count']}; incorrect {s['incorrect_count']}; accuracy {s['accuracy_exact']}.", ""]
    lines += ["No singleton population was counted as success and no candidate was manufactured. Physical authority was opened only after exact blind replay. Historical evidence, H02, H03, physical authority, architecture and production code remain unchanged.", ""]
    (RUN / "report.md").write_text("\n".join(lines))
    artifacts = ["execute.py", "input_manifest.json", "observed_populations_without_strength.json", "blind_candidate_populations.json", "blind_strength_predictions.json", "event_level_scoring.json", "source_summary.json", "scientific_content.json", "result.json", "completion_protocol.json", "report.md"]
    write_json(RUN / "artifact_manifest.json", {"study_id": STUDY_ID, "scientific_fingerprint": scientific_fp, "artifacts": {name: checksum(RUN / name) for name in artifacts}})
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
