"""Score the checksum-frozen CED-VAL-002 blind H02 population only."""

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
BLIND = RUN / "blind_result.json"
BLIND_MANIFEST = RUN / "blind_manifest.json"
CALIBRATION = ROOT / "validation/CED-VAL-002-SWING/run_20260823_170857"
ABSOLUTE = CALIBRATION / "event_level_results.json"
PAIR_AUTHORITY = CALIBRATION / "symbolic_pair_authority.json"
PAIR_RESULTS = CALIBRATION / "event_pair_results.json"
EXPECTED = {"blind": "e2ad20937b6d623f40c05e9df30eb59bb9e07deee5c91d316a38647b6bfb27ef", "absolute": "cf6aace090c92c3077b642bd6f8506b1a8516c4e55743a797581b763fbd71ecc", "pair_authority": "f00958d9f534135273cb33fc0d533e07864f1ff964b62ce6512dd4209a327a96", "pair_results": "6b1b67723dd2414674bd6913f06cedb71afe668dde70a71cc158a98e4df4c962"}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def metrics(tp: int, fp: int, fn: int) -> dict:
    precision = None if tp + fp == 0 else tp / (tp + fp)
    recall = None if tp + fn == 0 else tp / (tp + fn)
    f1 = None if precision is None or recall is None or precision + recall == 0 else 2 * precision * recall / (precision + recall)
    return {"tp": tp, "fp": fp, "fn": fn, "precision": precision, "recall": recall, "f1": f1}


def classify(by_source: dict, overall: dict) -> str:
    if overall["scorable_candidate_count"] == 0 or any(item["scorable_candidate_count"] == 0 for item in by_source.values()):
        return "INSUFFICIENT_CANDIDATES"
    if overall["precision"] == 1.0 and all(item["precision"] == 1.0 for item in by_source.values()):
        return "HIGH_PRECISION_USEFUL_CANDIDATE_RULE"
    if overall["precision"] is not None and overall["fp"] >= overall["tp"]:
        return "LOW_PRECISION"
    if overall["precision"] is not None and overall["precision"] > 0.5 and overall["recall"] is not None and overall["fn"] >= overall["tp"]:
        return "LOW_RECALL"
    return "PARTIAL_CORRESPONDENCE_EVIDENCE"


def main() -> None:
    manifest = json.loads(BLIND_MANIFEST.read_text())
    actual = {"blind": digest(BLIND), "absolute": digest(ABSOLUTE), "pair_authority": digest(PAIR_AUTHORITY), "pair_results": digest(PAIR_RESULTS)}
    if actual != EXPECTED or manifest["blind_result_sha256"] != actual["blind"] or manifest["ground_truth_accessed"]:
        raise RuntimeError(f"frozen scoring authority mismatch: {actual}")
    blind = json.loads(BLIND.read_text())
    if blind["blind_scientific_fingerprint"] != manifest["blind_scientific_fingerprint"]:
        raise RuntimeError("blind fingerprint mismatch")
    absolute = json.loads(ABSOLUTE.read_text())
    pair_authority = json.loads(PAIR_AUTHORITY.read_text())
    pair_results = json.loads(PAIR_RESULTS.read_text())
    candidates = blind["scientific_content"]["candidates"]
    eme_to_symbolic = {source: {record["eme_id"]: record["calibration_symbolic_event_id"] for record in payload["valid_records"]} for source, payload in absolute["correspondence_by_source"].items()}
    by_source, score_records = {}, {}
    for source in ("Piano", "Double Bass"):
        valid_pairs = [record for record in pair_results["pairs_by_source"][source] if record["jga_pair_status"] == "VALID_JGA_PAIR"]
        authorized = {(record["source_symbolic_event_id"], record["drum_symbolic_event_id"]): record for record in valid_pairs}
        source_candidates = [record for record in candidates if record["contributor"] == source]
        records, recovered = [], set()
        tp = fp = ambiguous = 0
        for candidate in source_candidates:
            source_eme, drum_eme = candidate["target"]["eme_id"], candidate["drum"]["eme_id"]
            source_symbolic = eme_to_symbolic[source].get(source_eme)
            drum_symbolic = eme_to_symbolic["Drums"].get(drum_eme)
            if source_symbolic is None or drum_symbolic is None:
                score, pair = "AMBIGUOUS_UNSCORABLE", None
                ambiguous += 1
            else:
                pair = authorized.get((source_symbolic, drum_symbolic))
                score = "TRUE_POSITIVE" if pair is not None else "FALSE_POSITIVE"
                tp += pair is not None
                fp += pair is None
                if pair is not None:
                    recovered.add(pair["symbolic_pair_id"])
            records.append({"source": source, "source_eme_id": source_eme, "drum_eme_id": drum_eme, "source_symbolic_event_id": source_symbolic, "drum_symbolic_event_id": drum_symbolic, "symbolic_pair_id": None if pair is None else pair["symbolic_pair_id"], "score": score})
        missed = [record for record in valid_pairs if record["symbolic_pair_id"] not in recovered]
        records.extend({"source": source, "source_eme_id": record["source_eme_id"], "drum_eme_id": record["drum_eme_id"], "source_symbolic_event_id": record["source_symbolic_event_id"], "drum_symbolic_event_id": record["drum_symbolic_event_id"], "symbolic_pair_id": record["symbolic_pair_id"], "score": "FALSE_NEGATIVE"} for record in missed)
        unresolved_symbolic = sum(record["status"] == "VALID_SYMBOLIC_PAIR" and record["jga_pair_status"] != "VALID_JGA_PAIR" for record in pair_results["pairs_by_source"][source])
        by_source[source] = {"blind_candidate_count": len(source_candidates), "unresolved_count": sum(record["contributor"] == source for record in blind["scientific_content"]["unresolved"]), "scorable_candidate_count": tp + fp, "ambiguous_unscorable_candidate_count": ambiguous, "ambiguous_unscorable_symbolic_relation_count": unresolved_symbolic, **metrics(tp, fp, len(missed))}
        score_records[source] = records
    overall = metrics(sum(item["tp"] for item in by_source.values()), sum(item["fp"] for item in by_source.values()), sum(item["fn"] for item in by_source.values()))
    overall.update({"blind_candidate_count": len(candidates), "unresolved_count": len(blind["scientific_content"]["unresolved"]), "scorable_candidate_count": sum(item["scorable_candidate_count"] for item in by_source.values()), "ambiguous_unscorable_candidate_count": sum(item["ambiguous_unscorable_candidate_count"] for item in by_source.values()), "ambiguous_unscorable_symbolic_relation_count": sum(item["ambiguous_unscorable_symbolic_relation_count"] for item in by_source.values())})
    result = {"schema": "H02-CEDVAL002-out-of-sample-result/v1", "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02", "validation_dataset": "PR-CED-VAL-002-SWING-002", "frozen_h02_preregistration_commit": "ca9683c786b8dbf57ea78f07ee16c86a896e3dbc", "blind_result_sha256": actual["blind"], "blind_scientific_fingerprint": blind["blind_scientific_fingerprint"], "ground_truth_scoring_authority": {"calibration_symbolic_event_fingerprint": "7fb4e7f3cbe8ecfa93fcfd9774256219daba2c4c1c70d07e04d913cb5e779642", "symbolic_pair_authority_sha256": actual["pair_authority"], "symbolic_pair_authority_fingerprint": pair_authority["scientific_fingerprint"], "absolute_correspondence_results_sha256": actual["absolute"], "pair_event_results_sha256": actual["pair_results"]}, "by_source": by_source, "overall": overall, "score_records": score_records, "outcome_classification": classify(by_source, overall), "ced_val_001_reference": {"candidate_count": 13, "tp": 12, "fp": 1, "precision": 0.923077, "recall": 0.222222, "f1": 0.358209}, "calibration_context_used_for_candidate_generation": False, "calibration_correction_applied": False, "ground_truth_used_for_scoring_only": True, "production_authorized_event_relation_promotion": False, "raw_observations_modified": False, "production_code_modified": False, "deterministic_replay": blind["deterministic_replay"]}
    result["scientific_fingerprint"] = sha256(canonical(result)).hexdigest()
    (RUN / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"by_source": by_source, "overall": overall, "outcome": result["outcome_classification"], "scientific_fingerprint": result["scientific_fingerprint"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
