"""Independently verify frozen CED-VAL-004 physical-onset artifacts."""

from hashlib import sha256
import json
from pathlib import Path

import execute


RUN = Path(__file__).parent


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def main() -> None:
    _, schedule, source_data, control_data, verified = execute.verify_inputs()
    replay_one = execute.analyze_once(schedule, source_data, control_data)
    replay_two = execute.analyze_once(schedule, source_data, control_data)
    frozen = json.loads((RUN / "event_level_physical_onsets.json").read_text())
    summary = execute.source_summary(replay_one)
    result = json.loads((RUN / "result.json").read_text())
    assert replay_one == replay_two == frozen["records"]
    assert summary == result["source_summary"] == json.loads((RUN / "source_summary.json").read_text())
    basis = {
        "dataset_fingerprint": execute.DATASET_FINGERPRINT,
        "schedule_fingerprint": verified["schedule_fingerprint"],
        "rule_id": execute.RULE_ID,
        "records": replay_one,
        "summary": summary,
        "provenance": frozen["provenance"],
    }
    fingerprint = sha256(canonical(basis)).hexdigest()
    assert fingerprint == frozen["scientific_fingerprint"] == result["scientific_fingerprint"]
    assert len(replay_one) == 20
    assert all(item["baseline"]["exact_zero"] for item in replay_one)
    assert not any(item["status"] == "AUTHORITY_CONFLICT" for item in replay_one)
    manifest = json.loads((RUN / "artifact_manifest.json").read_text())
    for name, expected in manifest["artifacts"].items():
        assert execute.checksum(RUN / name) == expected, name
    assert manifest["scientific_fingerprint"] == fingerprint
    print(f"PASS exact replay; fingerprint={fingerprint}")


if __name__ == "__main__":
    main()
