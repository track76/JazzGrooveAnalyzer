"""Execute frozen CED-VAL-003 H02 scorability authority audit."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
H02 = ROOT / "validation/CED-VAL-003-SWING-3-4/run_20260823_204545"
CAL = ROOT / "validation/CED-VAL-003-SWING-3-4/run_20260823_203324"
INPUTS = {
    "preregistration": (ROOT / "validation/CED-VAL-003-SWING-3-4/preregistrations/AUD-CEDVAL003-H02-SCORABILITY-01.md", "4dfa806eea4a3a268f9b41133506922b3b0fbca23cb8d859dde4159776a49614"),
    "blind_result": (H02 / "blind_result.json", "061968ece6e534d097b18936488c4fa551b216e9bb55beece4ba87cf8f13172a"),
    "scoring_result": (H02 / "result.json", "993fd8c05285e2402c03f7e813f3dfbbc30e54c40a5577e195c9c31997796828"),
    "event_results": (CAL / "event_level_results.json", "3c2d22300de63de57885a1c786dea1679136410860558f3e093e6bf2b5233c31"),
    "pair_authority": (CAL / "symbolic_pair_authority.json", "10cee0e96fc21b854714f426ca27543b94a63071b19861c7e28832f7e790fbf7"),
    "pair_results": (CAL / "event_pair_results.json", "a25cb0179f0f527b86d309d06da2c8ebb33d2e1afda63d0ff54ce5f5d7059a8e"),
    "three_dataset_conclusion": (ROOT / "validation/H02_THREE_DATASET_SCIENTIFIC_CONCLUSION.md", "f416d8efc8c10b520bc5257a475f075b022ba343ff1c615e6316798afd2d686c"),
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def authority_inventory(events: dict) -> dict:
    inventory = {}
    for source, payload in events["correspondence_by_source"].items():
        for record in payload["valid_records"]:
            inventory[record["eme_id"]] = {"source": source, "status": "VALID", "calibration_symbolic_event_id": record["calibration_symbolic_event_id"], "cell_index": record["cell_index"], "candidate_count": 1, "pulse_candidate_ids": record["supporting_pulse_candidate_ids"]}
        for cell in payload["event_results"]:
            for candidate in cell.get("candidate_emes", []):
                identity = candidate["eme_id"]
                if identity in inventory:
                    raise RuntimeError(f"duplicate EME authority: {identity}")
                inventory[identity] = {"source": source, "status": cell["correspondence_status"], "calibration_symbolic_event_id": cell["calibration_symbolic_event_id"], "cell_index": cell["cell_index"], "candidate_count": len(cell.get("candidate_emes", [])), "pulse_candidate_ids": candidate["supporting_pulse_candidate_ids"]}
        for record in payload["boundary_results"]:
            inventory[record["eme_id"]] = {"source": source, "status": "AMBIGUOUS_BOUNDARY", "calibration_symbolic_event_id": None, "cell_index": None, "candidate_count": 1, "pulse_candidate_ids": record["supporting_pulse_candidate_ids"]}
        for record in payload["unmatched_observed"]:
            inventory[record["eme_id"]] = {"source": source, "status": "UNMATCHED_OBSERVED", "calibration_symbolic_event_id": None, "cell_index": None, "candidate_count": 1, "pulse_candidate_ids": record["supporting_pulse_candidate_ids"]}
    return inventory


def build() -> dict:
    checks = {name: digest(path) for name, (path, _expected) in INPUTS.items()}
    if any(checks[name] != expected for name, (_path, expected) in INPUTS.items()):
        raise RuntimeError(f"frozen input mismatch: {checks}")
    blind = json.loads(INPUTS["blind_result"][0].read_text())["scientific_content"]
    scoring = json.loads(INPUTS["scoring_result"][0].read_text())
    events = json.loads(INPUTS["event_results"][0].read_text())
    pair_authority = json.loads(INPUTS["pair_authority"][0].read_text())
    pairs = json.loads(INPUTS["pair_results"][0].read_text())
    inventory = authority_inventory(events)
    scoring_candidates = {}
    for source, records in scoring["score_records"].items():
        for record in records:
            key = (source, record.get("source_eme_id"), record.get("drum_eme_id"))
            if record["score"] != "FALSE_NEGATIVE":
                if key in scoring_candidates:
                    raise RuntimeError(f"duplicate scoring join: {key}")
                scoring_candidates[key] = record
    pair_lookup = {(r["source"], r["source_symbolic_event_id"], r.get("drum_symbolic_event_id")): r for r in pair_authority["records"] if r["status"] == "VALID_SYMBOLIC_PAIR"}
    cases = []
    for candidate in blind["candidates"]:
        source = candidate["contributor"]
        source_id, drum_id = candidate["target"]["eme_id"], candidate["drum"]["eme_id"]
        score = scoring_candidates.get((source, source_id, drum_id))
        source_auth, drum_auth = inventory.get(source_id), inventory.get(drum_id)
        if score is None or source_auth is None or drum_auth is None:
            cause = "IDENTITY_PROVENANCE_JOIN_FAILURE"
            high = "INDETERMINATE"
        elif source_auth["status"] == drum_auth["status"] == "VALID":
            cause = "SCORABLE"
            high = "NOT_APPLICABLE_SCORABLE"
        elif source_auth["status"] == "VALID":
            cause = "DRUM_CALIBRATION_AUTHORITY_UNRESOLVED"
            high = "CALIBRATION_SCORING_AUTHORITY_LIMITATION"
        elif drum_auth["status"] == "VALID":
            cause = "ACCOMPANIMENT_CALIBRATION_AUTHORITY_UNRESOLVED"
            high = "CALIBRATION_SCORING_AUTHORITY_LIMITATION"
        else:
            cause = "BOTH_CALIBRATION_AUTHORITIES_UNRESOLVED"
            high = "CALIBRATION_SCORING_AUTHORITY_LIMITATION"
        source_symbolic = None if source_auth is None else source_auth["calibration_symbolic_event_id"]
        drum_symbolic = None if drum_auth is None else drum_auth["calibration_symbolic_event_id"]
        pair = pair_lookup.get((source, source_symbolic, drum_symbolic)) if source_symbolic and drum_symbolic else None
        cases.append({"source": source, "source_eme_id": source_id, "drum_eme_id": drum_id, "blind_status": candidate["status"], "frozen_score": None if score is None else score["score"], "source_authority": source_auth, "drum_authority": drum_auth, "cause": cause, "high_level_category": high, "exact_symbolic_pair_authority_id": None if pair is None else pair["symbolic_pair_id"], "candidate_identity_and_lineage_complete": bool(candidate["target"]["supporting_pulse_candidate_ids"] and candidate["drum"]["supporting_pulse_candidate_ids"]), "candidate_changed": False, "score_changed": False})
    symbolic_unresolved = []
    for source, records in pairs["pairs_by_source"].items():
        for record in records:
            if record["status"] == "VALID_SYMBOLIC_PAIR" and record["jga_pair_status"] != "VALID_JGA_PAIR":
                symbolic_unresolved.append({key: record.get(key) for key in ("source", "symbolic_pair_id", "source_symbolic_event_id", "drum_symbolic_event_id", "source_absolute_correspondence_status", "drum_absolute_correspondence_status", "jga_pair_status")})
    by_source = {}
    for source in ("Piano", "Double Bass"):
        selected = [c for c in cases if c["source"] == source]
        unscorable = [c for c in selected if c["frozen_score"] == "AMBIGUOUS_UNSCORABLE"]
        by_source[source] = {"blind_candidates": len(selected), "scorable": len(selected) - len(unscorable), "unscorable": len(unscorable), "cause_counts": dict(sorted(Counter(c["cause"] for c in unscorable).items())), "source_side_nonvalid": sum(c["source_authority"]["status"] != "VALID" for c in unscorable), "drum_side_nonvalid": sum(c["drum_authority"]["status"] != "VALID" for c in unscorable), "exact_symbolic_pair_authority_available": sum(c["exact_symbolic_pair_authority_id"] is not None for c in unscorable)}
    unscorable = [c for c in cases if c["frozen_score"] == "AMBIGUOUS_UNSCORABLE"]
    high = Counter(c["high_level_category"] for c in unscorable)
    summary = {"audit_population": {"blind_candidates": len(cases), "blind_unresolved": len(blind["unresolved"]), "unscorable_candidates": len(unscorable), "unscorable_symbolic_relations": len(symbolic_unresolved)}, "by_source": by_source, "cause_counts": dict(sorted(Counter(c["cause"] for c in unscorable).items())), "direct_status_counts": {"source": dict(sorted(Counter(c["source_authority"]["status"] for c in unscorable).items())), "drum": dict(sorted(Counter(c["drum_authority"]["status"] for c in unscorable).items()))}, "high_level_counts": {"candidate_discovery_limitation": high["CANDIDATE_DISCOVERY_LIMITATION"], "calibration_scoring_authority_limitation": high["CALIBRATION_SCORING_AUTHORITY_LIMITATION"], "mixed_limitation": high["MIXED_LIMITATION"], "indeterminate": high["INDETERMINATE"]}, "identity_provenance_join_failures": sum(c["cause"] == "IDENTITY_PROVENANCE_JOIN_FAILURE" for c in cases), "all_unscorable_explained": all(c["high_level_category"] != "INDETERMINATE" for c in unscorable), "frozen_metrics_changed": False, "candidates_changed": False, "h02_changed": False, "h03_created": False, "calibration_zero_changed": False, "raw_observations_changed": False, "production_code_changed": False}
    return {"schema": "JGA-H02-SCORABILITY-AUDIT/v1", "audit_id": "AUD-CEDVAL003-H02-SCORABILITY-01", "status": "PASS_FROZEN_READ_ONLY_AUDIT", "input_checksums": checks, "blind_fingerprint": "a76e37eda621a266832a4fd347b9ac7334a3d12e2c94351dfdc5fa1dd9faa997", "scoring_fingerprint": scoring["scientific_fingerprint"], "cases": cases, "unscorable_symbolic_relations": symbolic_unresolved, "summary": summary}


def main() -> None:
    first, second = build(), build()
    if canonical(first) != canonical(second):
        raise RuntimeError("deterministic audit replay failed")
    fingerprint = sha256(canonical(first)).hexdigest()
    result = {**first, "deterministic_replay": True, "audit_scientific_fingerprint": fingerprint}
    (RUN / "audit_result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": result["summary"], "fingerprint": fingerprint}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
