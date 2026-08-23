"""Verify symbolic pair authority without loading JGA observations."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/VAL-001/run_20260823_095617")
SOURCE = Path("validation/VAL-001/run_20260823_070702/calibration_symbolic_events.json")
PAIR_PATH = BASE / "symbolic_pair_authority.json"


def frac(record: dict) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def main() -> None:
    symbolic = json.loads(SOURCE.read_text())
    pair = json.loads(PAIR_PATH.read_text())
    drums: dict[Fraction, list[str]] = defaultdict(list)
    source_ids = set()
    for event in symbolic["events"]:
        source_ids.add(event["calibration_symbolic_event_id"])
        if event["source"] == "Drums":
            drums[frac(event["t_gt_seconds"])].append(
                event["calibration_symbolic_event_id"]
            )
    for record in pair["records"]:
        candidates = sorted(drums.get(frac(record["source_t_gt_seconds"]), []))
        assert record["source_symbolic_event_id"] in source_ids
        assert candidates == record["candidate_drum_symbolic_event_ids"]
        expected = (
            "VALID_SYMBOLIC_PAIR"
            if len(candidates) == 1
            else "UNMATCHED_SYMBOLIC_PAIR"
            if not candidates
            else "AMBIGUOUS_SYMBOLIC_PAIR"
        )
        assert record["status"] == expected
        assert record["drum_symbolic_event_id"] == (
            candidates[0] if len(candidates) == 1 else None
        )
    content = {
        "schema_revision": pair["schema_revision"],
        "source_authority_fingerprint": pair["source_authority_fingerprint"],
        "pair_rule": pair["pair_rule"],
        "records": pair["records"],
    }
    fingerprint = sha256(
        json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert fingerprint == pair["scientific_fingerprint"]
    assert pair["authority_status"] == "FROZEN"
    assert pair["jga_timestamps_accessed"] is False
    print("STATUS=PASS")
    print(f"SCIENTIFIC_FINGERPRINT={fingerprint}")
    print(json.dumps(pair["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
