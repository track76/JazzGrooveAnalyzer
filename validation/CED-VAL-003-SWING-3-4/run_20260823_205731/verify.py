"""Independent cardinality, join, cause and fingerprint verification."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


PATH = Path(__file__).with_name("audit_result.json")


def canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


result = json.loads(PATH.read_text())
fingerprint = result.pop("audit_scientific_fingerprint")
replay = result.pop("deterministic_replay")
assert replay is True
assert sha256(canonical(result)).hexdigest() == fingerprint
cases = result["cases"]
unscorable = [case for case in cases if case["frozen_score"] == "AMBIGUOUS_UNSCORABLE"]
assert len(cases) == 89 and len(unscorable) == 56
assert Counter(case["source"] for case in unscorable) == {"Double Bass": 47, "Piano": 9}
assert Counter(case["cause"] for case in unscorable) == {"DRUM_CALIBRATION_AUTHORITY_UNRESOLVED": 54, "ACCOMPANIMENT_CALIBRATION_AUTHORITY_UNRESOLVED": 2}
assert all(case["blind_status"] == "BLIND_CANDIDATE" for case in cases)
assert all(case["candidate_identity_and_lineage_complete"] for case in cases)
assert all(not case["candidate_changed"] and not case["score_changed"] for case in cases)
assert len(result["unscorable_symbolic_relations"]) == 55
assert result["summary"]["identity_provenance_join_failures"] == 0
assert result["summary"]["all_unscorable_explained"] is True
assert result["summary"]["high_level_counts"] == {"calibration_scoring_authority_limitation": 56, "candidate_discovery_limitation": 0, "indeterminate": 0, "mixed_limitation": 0}
print(f"STATUS=PASS\nAUDIT_CASES=89\nUNSCORABLE=56\nSYMBOLIC_UNSCORABLE=55\nFINGERPRINT={fingerprint}")
