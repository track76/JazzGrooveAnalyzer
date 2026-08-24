"""Verify frozen CED-VAL-004 prospective strength-prediction result."""
from hashlib import sha256
import json
from pathlib import Path

RUN = Path("validation/CED-VAL-004-PHYSICAL-ONSET/run_20260824_115749")

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def checksum(path):
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

result = json.loads((RUN / "result.json").read_text())
observed = json.loads((RUN / "observed_populations_without_strength.json").read_text())
populations = json.loads((RUN / "blind_candidate_populations.json").read_text())
predictors = json.loads((RUN / "blind_strength_predictions.json").read_text())
scoring = json.loads((RUN / "event_level_scoring.json").read_text())
scientific = json.loads((RUN / "scientific_content.json").read_text())
manifest = json.loads((RUN / "artifact_manifest.json").read_text())

assert result["classification"] == "INSUFFICIENT_NONVACUOUS_CANDIDATES"
assert result["scientific_fingerprint"] == sha256(canonical(scientific)).hexdigest()
assert len(populations["populations"]) == 20 == len(predictors["predictions"]) == len(scoring)
assert sum(len(observed[source]) for source in observed) == 20
assert all(len(observed[source]) == 10 for source in ("Drums", "Double Bass"))
assert all(row["population_status"] == "SINGLETON_CANDIDATE_POPULATION" for row in populations["populations"])
assert all(row["candidate_count"] == 1 and len(row["candidate_ids"]) == 1 for row in populations["populations"])
assert all(row["predictor_status"] is None and row["predicted_pulse_candidate_id"] is None and row["strengths"] == [] for row in predictors["predictions"])
assert all(row["scoring_status"] is None and row["distances"] == [] for row in scoring)
assert result["overall_summary"] == {"accuracy_exact": None, "correct_count": 0, "incorrect_count": 0, "non_vacuous_count": 0, "scorable_count": 0}
assert result["strength_values_accessed_count"] == 0
assert result["t_physical_opened_only_after_blind_freeze"] is True
assert result["deterministic_replay"] == "PASS_EXACT"
assert all(value is False for value in result["firewalls"].values())
for name, expected in manifest["artifacts"].items():
    if name != "verify.py":
        assert checksum(RUN / name) == expected
print(json.dumps({"status": "PASS", "population": "20/20 SINGLETON", "non_vacuous": 0, "strength_values_accessed": 0, "scorable": 0, "classification": result["classification"], "scientific_fingerprint": result["scientific_fingerprint"]}, indent=2))
