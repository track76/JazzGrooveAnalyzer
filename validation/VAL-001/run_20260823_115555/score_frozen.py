"""Post-freeze scoring for H-VAL001-RHYTHM-CORRESPONDENCE-02."""

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
BLIND = RUN / "blind_result.json"
BLIND_MANIFEST = RUN / "blind_manifest.json"
PAIR_RUN = ROOT / "validation/VAL-001/run_20260823_095617"
PAIR_AUTHORITY = PAIR_RUN / "symbolic_pair_authority.json"
PAIR_RESULTS = PAIR_RUN / "event_pair_results.json"
ABSOLUTE_RESULTS = ROOT / "validation/VAL-001/run_20260823_070702/event_level_results.json"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def metrics(tp, fp, fn):
    precision = None if tp + fp == 0 else tp / (tp + fp)
    recall = None if tp + fn == 0 else tp / (tp + fn)
    f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def classify(by_source, overall):
    if overall["scorable_candidate_count"] == 0 or any(item["scorable_candidate_count"] == 0 for item in by_source.values()):
        return "INSUFFICIENT_CANDIDATES"
    if overall["precision"] == 1.0 and all(item["precision"] == 1.0 for item in by_source.values()):
        return "HIGH_PRECISION_USEFUL_CANDIDATE_RULE"
    if overall["precision"] is not None and overall["fp"] >= overall["tp"]:
        return "LOW_PRECISION"
    if overall["precision"] is not None and overall["precision"] > 0.5 and overall["recall"] is not None and overall["fn"] >= overall["tp"]:
        return "LOW_RECALL"
    return "PARTIAL_CORRESPONDENCE_EVIDENCE"


def main():
    blind_manifest = json.loads(BLIND_MANIFEST.read_text())
    if digest(BLIND) != blind_manifest["blind_result_sha256"]:
        raise RuntimeError("Frozen blind artifact checksum mismatch")
    blind = json.loads(BLIND.read_text())
    if blind["blind_scientific_fingerprint"] != blind_manifest["blind_scientific_fingerprint"]:
        raise RuntimeError("Frozen blind fingerprint mismatch")
    pair_manifest = json.loads((PAIR_RUN / "artifact_manifest.json").read_text())
    if digest(PAIR_AUTHORITY) != pair_manifest["symbolic_pair_authority.json"] or digest(PAIR_RESULTS) != pair_manifest["event_pair_results.json"]:
        raise RuntimeError("Ground Truth authority checksum mismatch")

    authority = json.loads(PAIR_AUTHORITY.read_text())
    pair_results = json.loads(PAIR_RESULTS.read_text())
    absolute = json.loads(ABSOLUTE_RESULTS.read_text())
    candidates = blind["scientific_content"]["candidates"]
    eme_to_symbolic = {
        source: {item["eme_id"]: item["calibration_symbolic_event_id"] for item in evidence["valid_records"]}
        for source, evidence in absolute["correspondence_by_source"].items()
    }

    by_source, score_records = {}, {}
    for source in ("Piano", "Double Bass"):
        valid_pairs = [item for item in pair_results["records_by_source"][source] if item["jga_pair_status"] == "VALID_JGA_PAIR"]
        authorized_symbolic = {(item["source_symbolic_event_id"], item["drum_symbolic_event_id"]): item for item in valid_pairs}
        candidates_for_source = [item for item in candidates if item["contributor"] == source]
        records, recovered_ids = [], set()
        tp = fp = ambiguous = 0
        for candidate in candidates_for_source:
            source_eme = candidate["target"]["eme_id"]
            drum_eme = candidate["drum"]["eme_id"]
            source_symbolic = eme_to_symbolic[source].get(source_eme)
            drum_symbolic = eme_to_symbolic["Drums"].get(drum_eme)
            if source_symbolic is None or drum_symbolic is None:
                score, pair = "AMBIGUOUS_UNSCORABLE", None
                ambiguous += 1
            else:
                pair = authorized_symbolic.get((source_symbolic, drum_symbolic))
                score = "TRUE_POSITIVE" if pair is not None else "FALSE_POSITIVE"
                tp += pair is not None
                fp += pair is None
                if pair is not None:
                    recovered_ids.add(pair["symbolic_pair_id"])
            records.append({
                "source": source, "source_eme_id": source_eme, "drum_eme_id": drum_eme,
                "source_symbolic_event_id": source_symbolic,
                "drum_symbolic_event_id": drum_symbolic,
                "symbolic_pair_id": None if pair is None else pair["symbolic_pair_id"],
                "score": score,
            })
        missed = [item for item in valid_pairs if item["symbolic_pair_id"] not in recovered_ids]
        records.extend({
            "source": source, "source_eme_id": item["source_eme_id"],
            "drum_eme_id": item["drum_eme_id"],
            "source_symbolic_event_id": item["source_symbolic_event_id"],
            "drum_symbolic_event_id": item["drum_symbolic_event_id"],
            "symbolic_pair_id": item["symbolic_pair_id"], "score": "FALSE_NEGATIVE",
        } for item in missed)
        unresolved_symbolic = sum(
            item["status"] == "VALID_SYMBOLIC_PAIR" and item["jga_pair_status"] != "VALID_JGA_PAIR"
            for item in pair_results["records_by_source"][source]
        )
        by_source[source] = {
            "blind_candidate_count": len(candidates_for_source),
            "unresolved_count": sum(item["contributor"] == source for item in blind["scientific_content"]["unresolved"]),
            "scorable_candidate_count": tp + fp,
            "ambiguous_unscorable_candidate_count": ambiguous,
            "ambiguous_unscorable_symbolic_relation_count": unresolved_symbolic,
            **metrics(tp, fp, len(missed)),
        }
        score_records[source] = records

    overall = metrics(
        sum(item["tp"] for item in by_source.values()),
        sum(item["fp"] for item in by_source.values()),
        sum(item["fn"] for item in by_source.values()),
    )
    overall.update({
        "blind_candidate_count": len(candidates),
        "unresolved_count": len(blind["scientific_content"]["unresolved"]),
        "scorable_candidate_count": sum(item["scorable_candidate_count"] for item in by_source.values()),
        "ambiguous_unscorable_candidate_count": sum(item["ambiguous_unscorable_candidate_count"] for item in by_source.values()),
        "ambiguous_unscorable_symbolic_relation_count": sum(item["ambiguous_unscorable_symbolic_relation_count"] for item in by_source.values()),
    })
    outcome = classify(by_source, overall)
    result = {
        "schema": "H-VAL001-RHYTHM-CORRESPONDENCE-02-result/v1",
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02",
        "preregistration_commit": "62cebe2c46402d80803c82c4ea74d9b4d61006a7",
        "blind_result_sha256": digest(BLIND),
        "blind_scientific_fingerprint": blind["blind_scientific_fingerprint"],
        "ground_truth_scoring_authority": {
            "symbolic_pair_authority_sha256": digest(PAIR_AUTHORITY),
            "symbolic_pair_authority_fingerprint": authority["scientific_fingerprint"],
            "pair_event_results_sha256": digest(PAIR_RESULTS),
            "absolute_correspondence_results_sha256": digest(ABSOLUTE_RESULTS),
        },
        "candidate_comparison": {"hypothesis_01": 0, "hypothesis_02": len(candidates), "change": len(candidates)},
        "by_source": by_source, "overall": overall, "score_records": score_records,
        "outcome_classification": outcome,
        "production_authorized_event_relation_promotion": False,
        "raw_observations_modified": False,
        "production_code_modified": False,
        "ground_truth_used_for_scoring_only": True,
        "deterministic_replay": blind["deterministic_replay"],
    }
    result["scientific_fingerprint"] = sha256(canonical(result)).hexdigest()
    (RUN / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    artifact_manifest = {
        name: digest(RUN / name) for name in (
            "blind_execute.py", "blind_manifest.json", "blind_result.json",
            "score_frozen.py", "result.json", "report.md", "manifest.json",
            "verify.py",
        )
    }
    (RUN / "artifact_manifest.json").write_text(json.dumps(artifact_manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"by_source": by_source, "overall": overall, "outcome": outcome, "scientific_fingerprint": result["scientific_fingerprint"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
