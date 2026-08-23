"""Build frozen symbolic pair authority without accessing JGA observations."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/VAL-001/run_20260823_095617")
SOURCE = Path("validation/VAL-001/run_20260823_070702/calibration_symbolic_events.json")
OUTPUT = BASE / "symbolic_pair_authority.json"
EXPECTED_SOURCE_SHA = "038a970994dcb42961d115c6b5c7dd2a05c714b52f5fec3a1756133b5cdedd9f"
EXPECTED_SOURCE_FINGERPRINT = "b682fadc92be106fcf6b6a5379a4ab840c18e2bc8c852e44a4cda96c30488086"
PAIR_TYPES = ("Piano", "Double Bass", "Tenor Sax")


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def exact_time(event: dict) -> Fraction:
    value = event["t_gt_seconds"]
    return Fraction(value["numerator"], value["denominator"])


def pair_id(source: str, source_id: str, drum_id: str | None) -> str:
    content = ":".join(
        (EXPECTED_SOURCE_FINGERPRINT, source, source_id, drum_id or "NONE")
    )
    return "CSP-" + sha256(content.encode()).hexdigest()


def main() -> None:
    if checksum(SOURCE) != EXPECTED_SOURCE_SHA:
        raise RuntimeError("CalibrationSymbolicEvent checksum mismatch")
    authority = json.loads(SOURCE.read_text(encoding="utf-8"))
    if authority["scientific_fingerprint"] != EXPECTED_SOURCE_FINGERPRINT:
        raise RuntimeError("CalibrationSymbolicEvent fingerprint mismatch")
    if authority["jga_observed_events_accessed"]:
        raise RuntimeError("Symbolic authority was not observation-independent")

    drums_by_time: dict[Fraction, list[dict]] = defaultdict(list)
    source_events: dict[str, list[dict]] = defaultdict(list)
    for event in authority["events"]:
        source_events[event["source"]].append(event)
        if event["source"] == "Drums":
            drums_by_time[exact_time(event)].append(event)

    records = []
    for source in PAIR_TYPES:
        for event in source_events[source]:
            candidates = sorted(
                drums_by_time.get(exact_time(event), []),
                key=lambda item: item["calibration_symbolic_event_id"],
            )
            if len(candidates) == 1:
                status = "VALID_SYMBOLIC_PAIR"
                drum_id = candidates[0]["calibration_symbolic_event_id"]
            elif not candidates:
                status = "UNMATCHED_SYMBOLIC_PAIR"
                drum_id = None
            else:
                status = "AMBIGUOUS_SYMBOLIC_PAIR"
                drum_id = None
            records.append(
                {
                    "symbolic_pair_id": pair_id(
                        source,
                        event["calibration_symbolic_event_id"],
                        drum_id,
                    ),
                    "pair_type": f"{source}–Drums",
                    "source": source,
                    "source_symbolic_event_id": event[
                        "calibration_symbolic_event_id"
                    ],
                    "source_t_gt_seconds": event["t_gt_seconds"],
                    "status": status,
                    "drum_symbolic_event_id": drum_id,
                    "drum_t_gt_seconds": (
                        candidates[0]["t_gt_seconds"] if len(candidates) == 1 else None
                    ),
                    "candidate_drum_symbolic_event_ids": [
                        item["calibration_symbolic_event_id"] for item in candidates
                    ],
                }
            )

    records.sort(
        key=lambda item: (
            exact_time({"t_gt_seconds": item["source_t_gt_seconds"]}),
            item["source"],
            item["drum_symbolic_event_id"] or "",
            item["symbolic_pair_id"],
        )
    )
    scientific_content = {
        "schema_revision": "calibration-symbolic-pair-authority/v1",
        "source_authority_fingerprint": EXPECTED_SOURCE_FINGERPRINT,
        "pair_rule": "exact-rational-timestamp-equality/v1",
        "records": records,
    }
    fingerprint = sha256(
        json.dumps(scientific_content, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    counts = {}
    for source in PAIR_TYPES:
        selected = [record for record in records if record["source"] == source]
        counts[source] = {
            "symbolic_source_events": len(source_events[source]),
            "valid_symbolic_pairs": sum(
                record["status"] == "VALID_SYMBOLIC_PAIR" for record in selected
            ),
            "unmatched_symbolic_pairs": sum(
                record["status"] == "UNMATCHED_SYMBOLIC_PAIR" for record in selected
            ),
            "ambiguous_symbolic_pairs": sum(
                record["status"] == "AMBIGUOUS_SYMBOLIC_PAIR" for record in selected
            ),
        }
    payload = {
        **scientific_content,
        "authority_status": "FROZEN",
        "jga_timestamps_accessed": False,
        "counts": counts,
        "scientific_fingerprint": fingerprint,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("STATUS=FROZEN")
    print(f"SCIENTIFIC_FINGERPRINT={fingerprint}")
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
