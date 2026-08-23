"""Post-freeze scoring for H-VAL001-RHYTHM-CORRESPONDENCE-01."""

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


def main():
    blind_manifest = json.loads(BLIND_MANIFEST.read_text())
    if digest(BLIND) != blind_manifest["blind_result_sha256"]:
        raise RuntimeError("Frozen blind artifact checksum mismatch")
    blind = json.loads(BLIND.read_text())
    if blind["blind_scientific_fingerprint"] != blind_manifest["blind_scientific_fingerprint"]:
        raise RuntimeError("Frozen blind fingerprint mismatch")
    pair_manifest = json.loads((PAIR_RUN / "artifact_manifest.json").read_text())
    if digest(PAIR_AUTHORITY) != pair_manifest["symbolic_pair_authority.json"]:
        raise RuntimeError("Symbolic pair authority checksum mismatch")
    if digest(PAIR_RESULTS) != pair_manifest["event_pair_results.json"]:
        raise RuntimeError("Pairwise event results checksum mismatch")

    authority = json.loads(PAIR_AUTHORITY.read_text())
    pair_results = json.loads(PAIR_RESULTS.read_text())
    absolute = json.loads(ABSOLUTE_RESULTS.read_text())
    candidates = blind["scientific_content"]["candidates"]
    candidate_keys = {
        (item["contributor"], item["target"]["eme_id"], item["drum"]["eme_id"])
        for item in candidates
    }
    by_source = {}
    score_records = {}
    for source in ("Piano", "Double Bass"):
        valid_pairs = [item for item in pair_results["records_by_source"][source] if item["jga_pair_status"] == "VALID_JGA_PAIR"]
        unresolved_pairs = [item for item in pair_results["records_by_source"][source] if item["status"] == "VALID_SYMBOLIC_PAIR" and item["jga_pair_status"] != "VALID_JGA_PAIR"]
        authorized = {(source, item["source_eme_id"], item["drum_eme_id"]): item for item in valid_pairs}
        records = []
        tp = fp = 0
        for key in sorted(key for key in candidate_keys if key[0] == source):
            matched = authorized.get(key)
            records.append({
                "blind_relation": {"source": key[0], "source_eme_id": key[1], "drum_eme_id": key[2]},
                "score": "TRUE_POSITIVE" if matched else "FALSE_POSITIVE",
                "symbolic_pair_id": None if matched is None else matched["symbolic_pair_id"],
                "source_symbolic_event_id": None if matched is None else matched["source_symbolic_event_id"],
                "drum_symbolic_event_id": None if matched is None else matched["drum_symbolic_event_id"],
            })
            tp += matched is not None
            fp += matched is None
        recovered = set(key for key in candidate_keys if key in authorized)
        missed = [item for key, item in authorized.items() if key not in recovered]
        records.extend({
            "blind_relation": None, "score": "FALSE_NEGATIVE",
            "symbolic_pair_id": item["symbolic_pair_id"],
            "source_symbolic_event_id": item["source_symbolic_event_id"],
            "drum_symbolic_event_id": item["drum_symbolic_event_id"],
            "source_eme_id": item["source_eme_id"], "drum_eme_id": item["drum_eme_id"],
        } for item in missed)
        by_source[source] = {
            "blind_candidate_count": sum(key[0] == source for key in candidate_keys),
            "unresolved_count": sum(item["contributor"] == source for item in blind["scientific_content"]["unresolved"]),
            "scorable_candidate_count": tp + fp,
            "ambiguous_unscorable_candidate_count": 0,
            "ambiguous_unscorable_symbolic_relation_count": len(unresolved_pairs),
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
        "ambiguous_unscorable_candidate_count": 0,
        "ambiguous_unscorable_symbolic_relation_count": sum(item["ambiguous_unscorable_symbolic_relation_count"] for item in by_source.values()),
    })
    result = {
        "schema": "H-VAL001-RHYTHM-CORRESPONDENCE-01-result/v1",
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-01",
        "blind_result_sha256": digest(BLIND),
        "blind_scientific_fingerprint": blind["blind_scientific_fingerprint"],
        "ground_truth_scoring_authority": {
            "symbolic_pair_authority_sha256": digest(PAIR_AUTHORITY),
            "symbolic_pair_authority_fingerprint": authority["scientific_fingerprint"],
            "pair_event_results_sha256": digest(PAIR_RESULTS),
            "absolute_correspondence_results_sha256": digest(ABSOLUTE_RESULTS),
        },
        "by_source": by_source,
        "overall": overall,
        "score_records": score_records,
        "outcome_classification": "INSUFFICIENT_CANDIDATES",
        "production_authorized_event_relation_promotion": False,
        "raw_observations_modified": False,
        "ground_truth_used_for_scoring_only": True,
        "deterministic_replay": blind["deterministic_replay"],
    }
    scientific_fingerprint = sha256(canonical(result)).hexdigest()
    result["scientific_fingerprint"] = scientific_fingerprint
    output = RUN / "result.json"
    output.write_bytes(json.dumps(result, indent=2, sort_keys=True).encode() + b"\n")
    artifact_manifest = {
        name: digest(RUN / name) for name in (
            "blind_execute.py", "blind_manifest.json", "blind_result.json",
            "score_frozen.py", "result.json", "report.md", "manifest.json", "verify.py",
        )
    }
    (RUN / "artifact_manifest.json").write_text(json.dumps(artifact_manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"by_source": by_source, "overall": overall, "outcome": result["outcome_classification"], "scientific_fingerprint": scientific_fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
