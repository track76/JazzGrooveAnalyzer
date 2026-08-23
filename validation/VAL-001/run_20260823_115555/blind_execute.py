"""Blind execution of frozen H-VAL001-RHYTHM-CORRESPONDENCE-02."""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
PREREG = ROOT / "validation/VAL-001/preregistrations/H-VAL001-RHYTHM-CORRESPONDENCE-02.md"
H01_RUN = ROOT / "validation/VAL-001/run_20260823_111348"
EXPECTED_PREREG_SHA256 = "10f4f445b257a42e0bdb7cd98277ebbd6689c0f76315c04ca115b0f875e50784"
EXPECTED_H01_BLIND_SHA256 = "be4df39d565c61dfb4ac5226533d02c8e656add5d2d34fd57da161989ffc43ea"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def load_h01_blind_executor():
    path = H01_RUN / "blind_execute.py"
    spec = importlib.util.spec_from_file_location("h01_blind_executor", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def revised_failures(record):
    old = set(record["failure_reasons"])
    failures = {
        item for item in old
        if item.startswith("TARGET_TO_DRUM")
        or item == "DRUM_TO_TARGET_NEAREST_NOT_UNIQUE"
        or item.startswith("TARGET_SIGNATURE_")
        or item.startswith("DRUM_SIGNATURE_")
    }
    if record["target_signature"] is not None and record["target_signature_recurrence"] < 2:
        failures.add("TARGET_SIGNATURE_NOT_RECURRENT")
    if record["drum_signature"] is not None and record["drum_signature_recurrence"] < 2:
        failures.add("DRUM_SIGNATURE_NOT_RECURRENT")
    return sorted(failures)


def predicates(record):
    failures = set(record["failure_reasons"])
    target_unique = not any(item.startswith("TARGET_TO_DRUM") for item in failures)
    reverse_unique = "DRUM_TO_TARGET_NEAREST_NOT_UNIQUE" not in failures
    return {
        "valid_accompaniment_signature": record["target_signature"] is not None,
        "unique_target_to_drum": target_unique,
        "unique_drum_to_target": reverse_unique,
        "mutual_unique_nearest": target_unique and reverse_unique,
        "recurrent_drum_signature": record["drum_signature"] is not None and record["drum_signature_recurrence"] >= 2,
        "recurrent_accompaniment_signature": record["target_signature"] is not None and record["target_signature_recurrence"] >= 2,
        "complete_final_criterion": record["status"] == "BLIND_CANDIDATE",
    }


def gate_counts(records):
    order = (
        "valid_accompaniment_signature", "unique_target_to_drum",
        "unique_drum_to_target", "mutual_unique_nearest",
        "recurrent_drum_signature", "recurrent_accompaniment_signature",
        "complete_final_criterion",
    )
    tests = [predicates(item) for item in records]
    independent = {gate: sum(item[gate] for item in tests) for gate in order}
    alive = [True] * len(records)
    cumulative = {}
    for gate in order:
        alive = [survives and item[gate] for survives, item in zip(alive, tests)]
        cumulative[gate] = sum(alive)
    return {"independent": independent, "cumulative": cumulative}


def build_once():
    if digest(PREREG) != EXPECTED_PREREG_SHA256:
        raise RuntimeError("Frozen preregistration checksum mismatch")
    if digest(H01_RUN / "blind_result.json") != EXPECTED_H01_BLIND_SHA256:
        raise RuntimeError("Preceding frozen blind record checksum mismatch")

    # Reconstruct all raw blind authority and evidence using the audited H01
    # executor. No serialized H01 eligibility outcome is used as input.
    base = load_h01_blind_executor().build_once()
    source_records = base["candidates"] + base["unresolved"]
    records = []
    for old in source_records:
        record = dict(old)
        record["failure_reasons"] = revised_failures(old)
        record["status"] = "BLIND_CANDIDATE" if not record["failure_reasons"] else "UNRESOLVED"
        records.append(record)
    records.sort(key=lambda item: (item["contributor"], item["target"]["frame"], item["target"]["eme_id"]))
    candidates = [item for item in records if item["status"] == "BLIND_CANDIDATE"]
    unresolved = [item for item in records if item["status"] == "UNRESOLVED"]

    content = {
        "schema": "H-VAL001-RHYTHM-CORRESPONDENCE-02-blind/v1",
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02",
        "epistemic_status": "BLIND_FROZEN_NO_GROUND_TRUTH_ACCESS",
        "preregistration": {
            "commit": "62cebe2c46402d80803c82c4ea74d9b4d61006a7",
            "sha256": digest(PREREG),
        },
        "preceding_falsified_hypothesis": {
            "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-01",
            "blind_result_sha256": digest(H01_RUN / "blind_result.json"),
            "candidate_count": 0,
            "classification": "INSUFFICIENT_CANDIDATES",
        },
        "single_removed_condition": "EXACT_CROSS_SOURCE_SIGNATURE_EQUALITY",
        "authority_checks": base["authority_checks"],
        "configuration": base["configuration"],
        "profile": base["profile"],
        "population_counts": base["population_counts"],
        "frame_inventory": base["frame_inventory"],
        "signature_inventory": base["signature_inventory"],
        "recurrence_inventory": base["recurrence_inventory"],
        "candidates": candidates,
        "unresolved": unresolved,
        "gate_counts": {
            source: gate_counts([item for item in records if item["contributor"] == source])
            for source in ("Piano", "Double Bass")
        },
    }
    content["summary"] = {
        "candidate_counts": dict(Counter(item["contributor"] for item in candidates)),
        "candidate_total": len(candidates),
        "unresolved_counts": dict(Counter(item["contributor"] for item in unresolved)),
        "unresolved_total": len(unresolved),
        "failure_reason_counts": dict(sorted(Counter(reason for item in unresolved for reason in item["failure_reasons"]).items())),
        "candidate_change_from_hypothesis_01": len(candidates),
    }
    return content


def main():
    first, second = build_once(), build_once()
    first_bytes, second_bytes = canonical(first), canonical(second)
    if first_bytes != second_bytes:
        raise RuntimeError("Deterministic blind replay failed")
    fingerprint = sha256(first_bytes).hexdigest()
    envelope = {
        "blind_scientific_fingerprint": fingerprint,
        "deterministic_replay": True,
        "scientific_content": first,
    }
    output = RUN / "blind_result.json"
    output.write_bytes(canonical(envelope) + b"\n")
    manifest = {
        "experiment_id": "H-VAL001-RHYTHM-CORRESPONDENCE-02",
        "phase": "BLIND_FROZEN",
        "blind_result_sha256": digest(output),
        "blind_scientific_fingerprint": fingerprint,
        "ground_truth_accessed": False,
        "deterministic_replay": True,
    }
    (RUN / "blind_manifest.json").write_bytes(canonical(manifest) + b"\n")
    print(json.dumps({**first["summary"], "gate_counts": first["gate_counts"], **manifest}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
