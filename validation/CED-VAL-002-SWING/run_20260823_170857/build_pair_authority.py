"""Freeze exact-timestamp symbolic pair authority without loading JGA events."""

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


BASE = Path("validation/CED-VAL-002-SWING/run_20260823_170857")
SOURCE = BASE / "calibration_symbolic_events.json"
SOURCE_SHA256 = "ec65381a1de5850efb8a03eb993984659e9af33da6f7eb51b33785696d784ef7"
OUTPUT = BASE / "symbolic_pair_authority.json"


def checksum(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if checksum(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("symbolic authority checksum mismatch")
    authority = json.loads(SOURCE.read_text(encoding="utf-8"))
    drums = defaultdict(list)
    for event in authority["events"]:
        if event["source"] == "Drums":
            drums[event["t_gt_seconds"]["exact"]].append(event)
    records = []
    for source in ("Piano", "Double Bass"):
        for event in (item for item in authority["events"] if item["source"] == source):
            matches = drums[event["t_gt_seconds"]["exact"]]
            status = "VALID_SYMBOLIC_PAIR" if len(matches) == 1 else "UNMATCHED_SYMBOLIC_PAIR" if not matches else "AMBIGUOUS_SYMBOLIC_PAIR"
            payload = {"symbolic_authority_fingerprint": authority["scientific_fingerprint"], "source": source, "source_symbolic_event_id": event["calibration_symbolic_event_id"], "drum_symbolic_event_ids": sorted(match["calibration_symbolic_event_id"] for match in matches), "t_gt_seconds": event["t_gt_seconds"]["exact"], "status": status}
            identity = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            records.append({"symbolic_pair_id": f"CSP-{identity}", **payload, "drum_symbolic_event_id": matches[0]["calibration_symbolic_event_id"] if len(matches) == 1 else None})
    scientific = {"schema_revision": "1", "symbolic_authority_fingerprint": authority["scientific_fingerprint"], "sources": ["Piano", "Double Bass"], "rule": "exact-rational-timestamp-equality/v1", "records": records}
    fingerprint = sha256(json.dumps(scientific, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    counts = {source: {status: sum(record["source"] == source and record["status"] == status for record in records) for status in ("VALID_SYMBOLIC_PAIR", "UNMATCHED_SYMBOLIC_PAIR", "AMBIGUOUS_SYMBOLIC_PAIR")} for source in ("Piano", "Double Bass")}
    OUTPUT.write_text(json.dumps({**scientific, "counts": counts, "scientific_fingerprint": fingerprint}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "counts": counts, "scientific_fingerprint": fingerprint, "sha256": checksum(OUTPUT)}, sort_keys=True))


if __name__ == "__main__":
    main()
